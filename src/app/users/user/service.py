import typing as t
import uuid
from fastapi import Request, status
from fastapi import Response
from core.enum.sort_type import SearchType, SortOrder
from core.schema.response import ITotalCount, IResponseMessage
from src.app.auth.schema import ICheckUserEmail, IRefreshToken, IToken
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from src.app.auth import service as auth_service
from src.app.users.permission.model import Permission
from lib.errors import error
from src.app.users.user import schema, model
from src.app.users.user.repository import users_repo
from src.app.users.permission.repository import permission_repo
from src.taskiq.user import tasks
from lib.utils import security


async def create(data_in=schema.IUserIn):
    check_customer = await users_repo.get_by_attr(
        attr=dict(email=data_in.email), first=True
    )
    if check_customer:
        raise error.DuplicateError("Account already exist")
    else:
        check_customer = await users_repo.get_by_attr(
            attr=dict(username=data_in.username), first=True
        )
        if check_customer:
            raise error.DuplicateError("Account with this username already exist")
    new_customer = await users_repo.create(data_in)

    if new_customer:
        await tasks.send_users_activation_email.kiq(
            dict(
                email=new_customer.email,
                id=str(new_customer.id),
                full_name=f"{new_customer.firstname} {new_customer.lastname}"
                if new_customer.firstname and new_customer.lastname
                else new_customer.username,
            )
        )
        get_permission = await permission_repo.get_by_attr(
            attr=dict(name="user"), first=True
        )

        if not get_permission:
            get_permission = await permission_repo.create(
                dict(name="user"), expunge=False
            )
        await users_repo.add_users_permission(
            users_id=new_customer.id, permission_objs=[get_permission]
        )
        return IResponseMessage(
            message="Account was created successfully, check your email to activate your account"
        )
    raise error.ServerError("Could not create account, please try again")


async def update_user_details(data_in=schema.IUserUpdateIn):
    check_customer = await users_repo.get(id=data_in.id)
    if not check_customer:
        raise error.NotFoundError("Account does not exist")
    if data_in.email and check_customer.email != data_in.email:
        check_existing_email = await users_repo.get_by_attr(
            attr=dict(email=check_customer.email), first=True
        )
        if str(check_existing_email.id) != check_customer.id:
            raise error.BadDataError("Account with this email already exists")
    elif data_in.username and data_in.username != check_customer.username:
        check_username = await users_repo.get_by_attr(
            attr=dict(email=check_customer.email), first=True
        )
        if str(check_username.id) != check_customer.id:
            raise error.BadDataError("Account with this username already exists")
    users_update = await users_repo.update(
        user=check_customer,
        obj=data_in.dict(exclude={"id"}, exclude_unset=True),
    )

    if not users_update:
        raise error.ServerError("Could not updating  details, please try again")

    if users_update and data_in.email:
        await tasks.send_verify_users_password_reset.kiq(
            dict(
                email=users_update.email,
                id=str(users_update.id),
                full_name=f"{users_update.firstname} {users_update.lastname}"
                if users_update.firstname and users_update.lastname
                else users_update.username,
            )
        )
        return IResponseMessage(
            message="Account was updated successfully, please check your email to confirm your email shipping_address"
        )
    else:
        return IResponseMessage(
            message="Account was updated successfully, please check your email to activate your account"
        )


async def filter(
    filter: str = "",
    per_page: int = 10,
    page: int = 0,
    select: str = "",
    sort_by: SortOrder = SortOrder.asc,
    order_by: str = None,
    is_active: bool = False,
    load_related: bool = False,
) -> t.List[model.User]:
    get_customers = await users_repo.filter(
        filter_string=filter,
        per_page=per_page,
        page=page,
        select_columns=select,
        order_by=order_by,
        sort_by=sort_by,
        load_related=load_related,
        strict_search=dict(is_active=is_active),
    )

    return get_customers


async def verify_users_email(
    data_in: schema.IUserAccountVerifyToken,
) -> IResponseMessage:
    data: dict = security.JWTAUTH.data_decoder(encoded_data=data_in.token)
    if not data.get("user_id", None):
        raise error.BadDataError("Invalid token data")
    users_obj = await users_repo.get(data.get("user_id", None))
    if not users_obj:
        raise error.BadDataError("Invalid token")

    if users_obj and users_obj.is_verified:
        raise error.BadDataError(
            detail="Account has been already verified",
        )
    users_obj = await users_repo.activate(users_obj)
    if users_obj:
        return IResponseMessage(message="Account was verified successfully")
    raise error.ServerError("Could not activate account, please try again")


async def reset_password_link(
    data_in: schema.IGetPasswordResetLink,
) -> IResponseMessage:
    users_obj = await users_repo.get_by_attr(attr=dict(email=data_in.email), first=True)
    if not users_obj.is_verified:
        await tasks.send_users_activation_email.kiq(
            user=dict(
                email=users_obj.email,
                id=str(users_obj.id),
                full_name=f"{users_obj.firstname} {users_obj.lastname}",
            )
        )
        return IResponseMessage(
            message="account need to be verified, before reset their password"
        )
    if not users_obj:
        raise error.NotFoundError("User not found")
    await tasks.send_users_password_reset_link.kiq(
        dict(
            email=users_obj.email,
            id=str(users_obj.id),
            full_name=f"{users_obj.firstname} {users_obj.lastname}",
        )
    )
    return IResponseMessage(
        message="Password reset token has been sent to your email, link expire after 24 hours"
    )


async def update_users_password(
    data_in: schema.IUserResetPassword,
) -> IResponseMessage:
    token_data: dict = security.JWTAUTH.data_decoder(encoded_data=data_in.token)
    if token_data and token_data.get("user_id", None):
        users_obj = await users_repo.get(token_data.get("user_id", None))
        if not users_obj:
            raise error.NotFoundError("User not found")
        if users_obj.password_reset_token != data_in.token:
            raise error.UnauthorizedError()
        if users_obj.check_password(data_in.password.get_secret_value()):
            raise error.BadDataError("Try another password you have not used before")
        if await users_repo.update_password(users_obj, data_in):
            await tasks.send_verify_users_password_reset.kiq(
                dict(
                    email=users_obj.email,
                    id=str(users_obj.id),
                    full_name=f"{users_obj.firstname} {users_obj.lastname}",
                )
            )
            return IResponseMessage(message="password was reset successfully")
    raise error.BadDataError("Invalid token was provided")


async def update_users_password_no_token(
    data_in: schema.IUserResetPasswordNoToken, user_data: model.User
) -> IResponseMessage:
    users_obj = await users_repo.get(user_data.id)
    if not users_obj:
        raise error.NotFoundError("User not found")

    if not users_obj.check_password(data_in.old_password.get_secret_value()):
        raise error.BadDataError("Old password is incorrect")

    if users_obj.check_password(data_in.password.get_secret_value()):
        raise error.BadDataError("Try another password you have not used before")
    if await users_repo.update_password(users_obj, data_in):
        await tasks.send_users_password_reset_link.kiq(
            dict(
                email=users_obj.email,
                id=str(users_obj.id),
                full_name=f"{users_obj.firstname} {users_obj.lastname}",
            )
        )
        return IResponseMessage(message="password was reset successfully")
    raise error.BadDataError("Invalid token was provided")


async def remove_users_data(data_in: schema.IUserRemove) -> None:
    users_to_remove = await users_repo.get(data_in.users_id)
    if users_to_remove:
        await users_repo.delete(user=users_to_remove, permanent=data_in.permanent)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise error.NotFoundError(f"User with  user id {data_in.users_id} does not exist")


async def get_total_customers():
    total_count = await users_repo.get_count()
    return ITotalCount(count=total_count).dict()


async def get_customer(users_id: uuid.UUID, load_related: bool = False) -> model.User:
    if not users_id:
        raise error.NotFoundError(
            f"User with  user id {users_id} does not exist",
        )
    use_detail = await users_repo.get(users_id, load_related=load_related)
    if use_detail:
        try:
            if not load_related:
                return schema.IUserOut.from_orm(use_detail)
            return schema.IUserOutFull.from_orm(use_detail)
        except Exception:
            raise error.ServerError("Error getting  user data")
    raise error.NotFoundError(
        f"User with id {users_id} does not exist",
    )


async def get_users_permissions(users_id: uuid.UUID) -> t.List[Permission]:
    use_detail = await users_repo.get(users_id, load_related=True)
    if use_detail:
        return use_detail.permissions
    raise error.NotFoundError(
        f"User with id {users_id} does not exist",
    )


async def add_users_permissions(
    data_in: schema.IUserRoleUpdate,
) -> IResponseMessage:
    get_per = await permission_repo.get_by_props(
        prop_name="id", prop_values=data_in.permissions
    )
    if not get_per:
        raise error.NotFoundError("permission not found")
    update_customer = await users_repo.add_users_permission(
        users_id=data_in.users_id,
        permission_objs=get_per,
    )
    if update_customer:
        return IResponseMessage(message=" user permission was updated successfully")


async def remove_users_permissions(
    data_in: schema.IUserRoleUpdate,
) -> IResponseMessage:
    check_perm = await permission_repo.get_by_ids(data_in.permissions)
    if not check_perm:
        raise error.NotFoundError(detail="Permission not found")
    await users_repo.remove_users_permission(
        users_id=data_in.users_id, permission_objs=check_perm
    )
    return IResponseMessage(message="User permission was updated successfully")


async def login(
    request: Request, data_in: OAuth2PasswordRequestForm
) -> t.Union[IToken, IResponseMessage]:
    check_user = await users_repo.get_by_attr(
        attr=dict(username=data_in.username, email=data_in.username),
        first=True,
        search_mode=SearchType._or,
    )
    if not check_user:
        raise error.UnauthorizedError(detail="incorrect email or password")
    if not check_user.check_password(data_in.password):
        raise error.UnauthorizedError(detail="incorrect email or password")
    if not check_user.is_verified:
        await tasks.send_users_activation_email.kiq(
            dict(email=data_in.username, id=str(check_user.id))
        )
        return IResponseMessage(
            message="Your is not verified, Please check your for verification link before continuing"
        )
    return await auth_service.auth_login(request=request, user_id=str(check_user.id))


async def login_token_refresh(data_in: IRefreshToken, request: Request) -> IToken:
    return await auth_service.auth_login_token_refresh(data_in=data_in, request=request)


async def check_user_email(data_in: ICheckUserEmail) -> IResponseMessage:
    check_user = await users_repo.get_by_attr(
        attr=dict(email=data_in.username, username=data_in.username),
        first=True,
        search_mode="or",
    )
    if not check_user:
        raise error.NotFoundError()
    return IResponseMessage(message="Account exists")
