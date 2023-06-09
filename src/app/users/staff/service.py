import typing as t
import uuid
from fastapi import status
from fastapi import Response
from core.enum.sort_type import SortOrder
from core.schema.response import ITotalCount, IResponseMessage
from src.app.users.permission.model import Permission
from lib.errors import error
from src.app.users.staff import schema, model
from src.app.users.staff.repository import staff_repo
from src.taskiq.staff import tasks
from src.app.users.permission.repository import permission_repo


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


async def remove_staff_data(data_in: schema.IRemoveStaff) -> None:
    staff_to_remove = await staff_repo.get(data_in.staff_id)
    if staff_to_remove:
        await staff_repo.delete(staff=staff_to_remove, permanent=data_in.permanent)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise error.NotFoundError(f"Staff with staff_id {data_in.staff_id} does not exist")


async def get_staff_details(
    staff_id: str, load_related: bool = False
) -> t.Union[schema.IStaffOutFull, schema.IStaffOut]:
    if not staff_id:
        raise error.NotFoundError(
            "staff  with  user does not exist",
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
