import typing as t
import uuid
from fastapi import Request, status
from fastapi import Response
from src._base.enum.sort_type import SortOrder
from src._base.schema.response import ITotalCount, IResponseMessage
from src._taskiq.user.tasks import send_customer_activation_email
from src.app.users.permission.model import Permission
from src.lib.errors import error
from src.app.users.staff import schema, model
from src.app.users.staff.repository import staff_repo
from src._taskiq.staff import tasks
from src.app.users.permission.repository import permission_repo
from src.lib.utils import security
from src.app.auth.schema import ICheckUserEmail, IRefreshToken, IToken
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from src.app.auth import service as auth_service


async def create(
    data_in=schema.IStaffIn,
):
    check_Staff = await staff_repo.get_by_email(data_in.email)
    if check_Staff:
        raise error.DuplicateError("Staff already exist")
    new_Staff = await staff_repo.create(data_in)
    if new_Staff:
        await tasks.send_staff_activation_email.kiq(
            staff=dict(
                email=new_Staff.email,
                id=str(new_Staff.id),
                full_name=f"{new_Staff.firstname} {new_Staff.lastname}",
            )
        )
    return IResponseMessage(
        message="Account was created successfully, please check your email to activate your account"
    )


async def filter(
    filter: str = "",
    per_page: int = 10,
    page: int = 0,
    select: str = "",
    sort_by: SortOrder = SortOrder.asc,
    order_by: str = None,
    is_active: bool = False,
) -> t.List[model.Staff]:
    get_staff = await staff_repo.filter(
        filter_string=filter,
        per_page=per_page,
        page=page,
        select_columns=select,
        order_by=order_by,
        sort_by=sort_by,
        strict_search=dict(is_active=is_active),
    )
    return get_staff


async def verify_staff_email(
    staff_token: schema.IStaffAccountVerifyToken,
) -> IResponseMessage:
    data: dict = security.JWTAUTH.data_decoder(encoded_data=staff_token.token)
    if not data.get("staff_id", None):
        raise error.BadDataError("Invalid token data")
    staff_obj = await staff_repo.get(data.get("staff_id", None))
    if staff_obj and staff_obj.is_verified:
        raise error.BadDataError(
            detail="Account has been already verified",
        )
    staff_obj = await staff_repo.activate(staff_obj)
    if staff_obj:
        return IResponseMessage(message="Account was verified successfully")
    raise error.ServerError(
        "couldn't activate account, please try again later. if error is persists please contact us"
    )


async def reset_password_link(
    staff_data: schema.IStaffGetPasswordResetLink,
) -> IResponseMessage:
    staff_obj = await staff_repo.get_by_email(email=staff_data.email)
    if not staff_obj:
        raise error.NotFoundError("Staff not found")
    await tasks.send_staff_password_reset_link.kiq(
        dict(
            email=staff_obj.email,
            id=str(staff_obj.id),
            full_name=f"{staff_obj.firstname} {staff_obj.lastname}",
        )
    )
    return IResponseMessage(
        message="Password reset token has been sent to your email, link expire after 24 hours"
    )


async def update_staff_password(
    staff_data: schema.IStaffResetPassword,
) -> IResponseMessage:
    token_data: dict = security.JWTAUTH.data_decoder(encoded_data=staff_data.token)
    if token_data:
        staff_obj = await staff_repo.get(token_data.get("staff_id", None))
        if not staff_obj:
            raise error.NotFoundError("Staff not found")
        if staff_obj.password_reset_token != staff_data.token:
            raise error.BadDataError("Authentication failed")
        if staff_obj.check_password(staff_data.password.get_secret_value()):
            raise error.BadDataError("Try another password you have not used before")
        if await staff_repo.update_password(staff_obj, staff_data):
            await tasks.send_verify_staff_password_reset.kiq(
                dict(
                    email=staff_obj.email,
                    id=str(staff_obj.id),
                    full_name=f"{staff_obj.firstname} {staff_obj.lastname}",
                )
            )
            return IResponseMessage(message="password was reset successfully")
    raise error.BadDataError("Invalid token was provided")


async def update_staff_password_tno_token(
    staff_data: schema.IStaffResetPasswordNoToken, staff: model.Staff
) -> IResponseMessage:
    staff_obj = await staff_repo.get(staff.id)
    if not staff_obj:
        raise error.NotFoundError("Staff not found")
    if staff_obj.check_password(staff_data.password.get_secret_value()):
        raise error.BadDataError("Try another password you have not used before")
    if await staff_repo.update_password(staff_obj, staff_data):
        await tasks.send_verify_staff_password_reset.kiq(
            dict(
                email=staff_obj.email,
                id=str(staff_obj.id),
                full_name=f"{staff_obj.firstname} {staff_obj.lastname}",
            )
        )
        return IResponseMessage(message="password was reset successfully")
    raise error.BadDataError("Invalid token was provided")


async def remove_staff_data(data_in: schema.IRemoveStaff) -> None:
    staff_to_remove = await staff_repo.get(data_in.staff_id)
    if staff_to_remove:
        await staff_repo.delete(staff=staff_to_remove, permanent=data_in.permanent)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise error.NotFoundError(f"Staff with staff_id {data_in.staff_id} does not exist")


async def get_staff(
    staff_id: str, load_related: bool = False
) -> t.Union[schema.IStaffOutFull, schema.IStaffOut]:
    if not staff_id:
        raise error.NotFoundError(
            "staff  with customer does not exist",
        )
    staffs = await staff_repo.get(staff_id, load_related=load_related)
    if staffs:
        try:
            if not load_related:
                return schema.IStaffOut.from_orm(staffs)
            return schema.IStaffOutFull.from_orm(staffs)
        except Exception:
            raise error.ServerError("Error getting staff data")
    raise error.NotFoundError("No staff with the provided credential")


async def get_total_Staffs():
    total_count = await staff_repo.get_count()
    return ITotalCount(count=total_count)


async def get_Staff(
    staff_id: uuid.UUID,
) -> model.Staff:
    use_detail = await staff_repo.get(staff_id, load_related=True)
    if use_detail:
        return use_detail
    raise error.NotFoundError(
        f"Staff with staff_id {staff_id} does not exist",
    )


async def add_staff_permission(
    data_in: schema.IStaffRoleUpdate,
) -> IResponseMessage:
    get_staff = await staff_repo.get(data_in.staff_id)
    if not get_staff:
        raise error.NotFoundError("Staff not found")
    get_perms = await permission_repo.get_by_props(
        prop_name="id", prop_values=data_in.permissions
    )
    if not get_perms:
        raise error.NotFoundError("permissions not found")
    update_Staff = await staff_repo.add_staff_permissions(
        staff_id=get_staff.id,
        permission_objs=get_perms,
    )
    if update_Staff:
        return IResponseMessage(message="Staff permission was updated successfully")


async def get_staff_permissions(
    staff_id: uuid.UUID,
) -> t.List[Permission]:
    check_Staff = await staff_repo.get(staff_id, load_related=True)
    if check_Staff:
        return check_Staff.permissions
    raise error.NotFoundError("Staff not found")


async def remove_staff_permissions(
    data_in: schema.IStaffRoleUpdate,
) -> IResponseMessage:
    get_staff = await staff_repo.get(data_in.staff_id, expunge=False)
    if not get_staff:
        raise error.NotFoundError("Staff not found")
    check_perms = await permission_repo.get_by_ids(data_in.permissions)
    if not check_perms:
        raise error.NotFoundError(detail=" Permission not found")
    await staff_repo.remove_staff_permission(
        staff_id=get_staff.id, permission_objs=check_perms
    )
    return IResponseMessage(message="Staff role was updated successfully")


async def login(
    request: Request, data_in: OAuth2PasswordRequestForm
) -> t.Union[IToken, IResponseMessage]:
    check_staff = await staff_repo.get_by_attr(
        attr=dict(email=data_in.username), first=True
    )
    if not check_staff:
        raise error.UnauthorizedError(detail="incorrect email or password")
    if not check_staff.check_password(data_in.password):
        raise error.UnauthorizedError(detail="incorrect email or password")
    if not check_staff.is_verified:
        await send_customer_activation_email.kiq(
            dict(email=data_in.username, id=str(check_staff.id))
        )
        return IResponseMessage(
            message="Your is not verified, Please check your for verification link before continuing"
        )
    return await auth_service.auth_login(request=request, user_id=str(check_staff.id))


async def login_token_refresh(data_in: IRefreshToken, request: Request) -> IToken:
    return await auth_service.auth_login_token_refresh(data_in=data_in, request=request)


async def check_user_email(data_in: ICheckUserEmail) -> IResponseMessage:
    check_staff = await staff_repo.get_by_attr(
        attr=dict(email=data_in.username), first=True
    )
    if not check_staff:
        raise error.NotFoundError()
    return IResponseMessage(message="Account exists")
