import typing as t
import uuid
from datetime import timedelta
from fastapi import status
from fastapi import BackgroundTasks, Response
from src._base.enum.sort_type import SortOrder
from src._base.schema.response import ITotalCount, IResponseMessage
from src.app.permission.model import Permission
from src.lib.errors import error
from src._base.settings import config
from src.app.staff import schema, model
from src.app.staff.repository import staff_repo
from src.dramatiq_tasks.tasks.staff import tasks
from src.app.permission.repository import permission_repo
from src.lib.shared.mail.mailer import Mailer
from src.lib.utils import security


async def create(
    data_in=schema.IStaffIn,
):
    check_Staff = await staff_repo.get_by_email(data_in.email)
    if check_Staff:
        raise error.DuplicateError("Staff already exist")
    new_Staff = await staff_repo.create(data_in)
    if new_Staff:
        tasks.send_staff_activation_email.send_with_options(
            kwargs=dict(
                email=new_Staff.email,
                id=str(new_Staff.id),
                full_name=f"{new_Staff.firstname} {new_Staff.lastname}",
            ),
            delay=5000,
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
    Staff_token: schema.IStaffAccountVerifyToken,
) -> IResponseMessage:
    data: dict = security.JWTAUTH.data_decoder(encoded_data=Staff_token.token)
    if not data.get("staff_id", None):
        raise error.BadDataError("Invalid token data")
    staff_obj = await staff_repo.get(data.get("staff_id", None))
    if staff_obj and staff_obj.is_active:
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
    tasks.send_staff_password_reset_link.send_with_options(
        kwargs=dict(
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
        if staff_obj.check_password(staff_data.password.get_secret_value()):
            raise error.BadDataError("Try another password you have not used before")
        if await staff_repo.update_password(staff_obj, staff_data):
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
        return IResponseMessage(message="password was reset successfully")
    raise error.BadDataError("Invalid token was provided")


async def remove_staff_data(data_in: schema.IRemoveStaff) -> None:
    staff_to_remove = await staff_repo.get(data_in.staff_id)
    if staff_to_remove:
        await staff_repo.delete(staff=staff_to_remove, permanent=data_in.permanent)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise error.NotFoundError(f"Staff with staff_id {data_in.staff_id} does not exist")


async def get_staff(staff_id: str, load_related: bool = False) -> t.List[model.Staff]:
    Staffs = await staff_repo.get(staff_id, load_related=load_related)
    return Staffs


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
        staff=get_staff,
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
    get_staff = await staff_repo.get(data_in.staff_id)
    if not get_staff:
        raise error.NotFoundError("Staff not found")
    check_perms = await permission_repo.get_by_ids(data_in.permissions)
    if not check_perms:
        raise error.NotFoundError(detail=" Permission not found")
    await staff_repo.remove_staff_permission(
        staff=get_staff, permission_objs=check_perms
    )
    return IResponseMessage(message="Staff role was updated successfully")
