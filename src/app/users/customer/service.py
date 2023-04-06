import typing as t
import uuid
from fastapi import Request, status
from fastapi import Response
from core.enum.sort_type import SearchType, SortOrder
from core.schema.response import ITotalCount, IResponseMessage
from lib.exceptions.duplicate_error import DuplicateError
from lib.exceptions.not_found_error import NotFoundError
from lib.exceptions.bad_input_data_error import BadDataError
from lib.exceptions.server_error import ServerError
from lib.exceptions.unauthorize_error import UnauthorizedError
from src.app.users.auth.schema import ICheckUserEmail, IRefreshToken, IToken
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from src.app.users.auth import service as auth_service
from src.app.users.permission.model import Permission
from src.app.users.customer import schema, model
from src.app.users.customer.query import customer_query
from src.app.users.permission.query import permission_query
from src.taskiq.user import tasks
from lib.utils import security


async def create(data_in=schema.ICustomerIn):
    check_customer = await customer_query.get_by_attr(email=data_in.email)
    if check_customer:
        raise DuplicateError("Account already exist")
    else:
        check_customer = await customer_query.get_by_attr(username=data_in.username)
        if check_customer:
            raise DuplicateError("Account with this username already exist")
    new_customer = await customer_query.create_obj(data_in)

    if new_customer:
        await tasks.send_customer_activation_email.kiq(
            dict(
                email=new_customer.email,
                id=str(new_customer.id),
                full_name=f"{new_customer.firstname} {new_customer.lastname}"
                if new_customer.firstname and new_customer.lastname
                else new_customer.username,
            )
        )
        get_permission = await permission_query.get_by_attr(name="customer")

        if not get_permission:
            get_permission = await permission_query.create_obj(name="customer")
        await customer_query.add_customer_permission(
            customer_id=new_customer.id, permission_objs=[get_permission]
        )
        return IResponseMessage(
            message="Account was created successfully, check your email to activate your account"
        )
    raise ServerError("Could not create account, please try again")


async def update_user_details(data_in=schema.ICustomerUpdateIn):
    check_customer = await customer_query.get_by_attr(id=data_in.id)
    if not check_customer:
        raise NotFoundError("Account does not exist")
    if data_in.email and check_customer.email != data_in.email:
        check_existing_email = await customer_query.get_by_attr(
            attr=dict(email=check_customer.email), first=True
        )
        if str(check_existing_email.id) != check_customer.id:
            raise BadDataError("Account with this email already exists")
    elif data_in.username and data_in.username != check_customer.username:
        check_username = await customer_query.get_by_attr(email=check_customer.email)
        if str(check_username.id) != check_customer.id:
            raise BadDataError("Account with this username already exists")
    customer_update = await customer_query.update_obj(
        customer=check_customer,
        obj=data_in.dict(exclude={"id"}, exclude_unset=True),
    )

    if not customer_update:
        raise ServerError("Could not updating  details, please try again")

    if customer_update and data_in.email:
        await tasks.send_verify_customer_password_reset.kiq(
            dict(
                email=customer_update.email,
                id=str(customer_update.id),
                full_name=f"{customer_update.firstname} {customer_update.lastname}"
                if customer_update.firstname and customer_update.lastname
                else customer_update.username,
            )
        )
        return IResponseMessage(
            message="Account was updated successfully, please check your email to confirm your email address"
        )
    else:
        return IResponseMessage(
            message="Account was updated successfully, please check your email to activate your account"
        )


async def filter(
    filter: str = "",
    page_size: int = 10,
    page: int = 0,
    select: str = "",
    sort_by: SortOrder = SortOrder.asc,
    order_by: str = None,
    is_active: bool = False,
    load_related: bool = False,
) -> t.List[model.Customer]:
    get_customers = await customer_query.filter(
        filter_string=filter,
        page_size=page_size,
        page=page,
        select_columns=select,
        order_by=order_by,
        sort_by=sort_by,
        load_related=load_related,
        strict_search=dict(is_active=is_active),
    )

    return get_customers


async def verify_customer_email(
    data_in: schema.ICustomerAccountVerifyToken,
) -> IResponseMessage:
    data: dict = security.JWTAUTH.data_decoder(encoded_data=data_in.token)
    if not data.get("user_id", None):
        raise BadDataError("Invalid token data")
    customer_obj = await customer_query.get_by_attr(id=data.get("user_id", None))
    if not customer_obj:
        raise BadDataError("Invalid token")

    if customer_obj and customer_obj.is_verified:
        raise BadDataError(
            detail="Account has been already verified",
        )
    customer_obj = await customer_query.activate(customer_obj)
    if customer_obj:
        return IResponseMessage(message="Account was verified successfully")
    raise ServerError("Could not activate account, please try again")


async def reset_password_link(
    data_in: schema.IGetPasswordResetLink,
) -> IResponseMessage:
    customer_obj = await customer_query.get_by_attr(email=data_in.email)
    if not customer_obj.is_verified:
        await tasks.send_customer_activation_email.kiq(
            customer=dict(
                email=customer_obj.email,
                id=str(customer_obj.id),
                full_name=f"{customer_obj.firstname} {customer_obj.lastname}",
            )
        )
        return IResponseMessage(
            message="account need to be verified, before reset their password"
        )
    if not customer_obj:
        raise NotFoundError("Customer not found")
    await tasks.send_customer_password_reset_link.kiq(
        dict(
            email=customer_obj.email,
            id=str(customer_obj.id),
            full_name=f"{customer_obj.firstname} {customer_obj.lastname}",
        )
    )
    return IResponseMessage(
        message="Password reset token has been sent to your email, link expire after 24 hours"
    )


async def update_customer_password(
    data_in: schema.ICustomerResetPassword,
) -> IResponseMessage:
    token_data: dict = security.JWTAUTH.data_decoder(encoded_data=data_in.token)
    if token_data and token_data.get("user_id", None):
        customer_obj = await customer_query.get_by_attr(
            id=token_data.get("user_id", None)
        )
        if not customer_obj:
            raise NotFoundError("Customer not found")
        if customer_obj.password_reset_token != data_in.token:
            raise UnauthorizedError()
        if customer_obj.check_password(data_in.password.get_secret_value()):
            raise BadDataError("Try another password you have not used before")
        if await customer_query.update_password(customer_obj, data_in):
            await tasks.send_verify_customer_password_reset.kiq(
                dict(
                    email=customer_obj.email,
                    id=str(customer_obj.id),
                    full_name=f"{customer_obj.firstname} {customer_obj.lastname}",
                )
            )
            return IResponseMessage(message="password was reset successfully")
    raise BadDataError("Invalid token was provided")


async def update_customer_password_no_token(
    data_in: schema.ICustomerResetPasswordNoToken, user_data: model.Customer
) -> IResponseMessage:
    customer_obj = await customer_query.get_by_attr(id=user_data.id)
    if not customer_obj:
        raise NotFoundError("Customer not found")

    if not customer_obj.check_password(data_in.old_password.get_secret_value()):
        raise BadDataError("Old password is incorrect")

    if customer_obj.check_password(data_in.password.get_secret_value()):
        raise BadDataError("Try another password you have not used before")
    if await customer_query.update_password(customer_obj, data_in):
        await tasks.send_customer_password_reset_link.kiq(
            dict(
                email=customer_obj.email,
                id=str(customer_obj.id),
                full_name=f"{customer_obj.firstname} {customer_obj.lastname}",
            )
        )
        return IResponseMessage(message="password was reset successfully")
    raise BadDataError("Invalid token was provided")


async def remove_customer_data(data_in: schema.ICustomerRemove) -> None:
    customer_to_remove = await customer_query.get_by_attr(id=data_in.customer_id)
    if customer_to_remove:
        await customer_query.delete(
            customer=customer_to_remove, permanent=data_in.permanent
        )
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise NotFoundError(
        f"Customer with customer id {data_in.customer_id} does not exist"
    )


async def get_total_customers():
    total_count = await customer_query.get_count()
    return ITotalCount(count=total_count).dict()


async def get_customer(
    customer_id: uuid.UUID, load_related: bool = False
) -> model.Customer:
    if not customer_id:
        raise NotFoundError(
            f"Customer with customer id {customer_id} does not exist",
        )
    use_detail = await customer_query.get_by_attr(
        id=customer_id, load_related=load_related
    )
    if use_detail:
        try:
            if not load_related:
                return schema.ICustomerOut.from_orm(use_detail)
            return schema.ICustomerOutFull.from_orm(use_detail)
        except Exception:
            raise ServerError("Error getting customer data")
    raise NotFoundError(
        f"User with id {customer_id} does not exist",
    )


async def get_customer_permissions(customer_id: uuid.UUID) -> t.List[Permission]:
    use_detail = await customer_query.get_by_attr(id=customer_id, load_related=True)
    if use_detail:
        return use_detail.permissions
    raise NotFoundError(
        f"User with id {customer_id} does not exist",
    )


async def add_customer_permissions(
    data_in: schema.ICustomerRoleUpdate,
) -> IResponseMessage:
    get_per = await permission_query.get_by_props(
        prop_name="id", prop_values=data_in.permissions
    )
    if not get_per:
        raise NotFoundError("permission not found")
    update_customer = await customer_query.add_customer_permission(
        customer_id=data_in.customer_id,
        permission_objs=get_per,
    )
    if update_customer:
        return IResponseMessage(message="customer permission was updated successfully")


async def remove_customer_permissions(
    data_in: schema.ICustomerRoleUpdate,
) -> IResponseMessage:
    check_perm = await permission_query.get_by_props(
        prop_name="id", prop_values=data_in.permissions
    )
    if not check_perm:
        raise NotFoundError(detail="Permission not found")
    await customer_query.remove_customer_permission(
        customer_id=data_in.customer_id, permission_objs=check_perm
    )
    return IResponseMessage(message="Customer permission was updated successfully")


async def login(
    request: Request, data_in: OAuth2PasswordRequestForm
) -> t.Union[IToken, IResponseMessage]:
    check_user = await customer_query.get_by_attr(
        username=data_in.username, email=data_in.username
    )
    if not check_user:
        raise UnauthorizedError(detail="incorrect email or password")
    if not check_user.check_password(data_in.password):
        raise UnauthorizedError(detail="incorrect email or password")
    if not check_user.is_verified:
        await tasks.send_customer_activation_email.kiq(
            dict(email=data_in.username, id=str(check_user.id))
        )
        return IResponseMessage(
            message="Your is not verified, Please check your for verification link before continuing"
        )
    return await auth_service.auth_login(request=request, user_id=str(check_user.id))


async def login_token_refresh(data_in: IRefreshToken, request: Request) -> IToken:
    return await auth_service.auth_login_token_refresh(data_in=data_in, request=request)


async def check_user_email(data_in: ICheckUserEmail) -> IResponseMessage:
    check_user = await customer_query.get_by_attr(
        email=data_in.username, username=data_in.username
    )
    if not check_user:
        raise NotFoundError()
    return IResponseMessage(message="Account exists")
