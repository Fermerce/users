import typing as t
from core.query.base_query import BaseQuery
from lib.exceptions.duplicate_error import DuplicateError
from lib.exceptions.not_found_error import NotFoundError
from src.app.users.permission.model import Permission
from src.app.users.staff import model, schema


class StaffQuery(BaseQuery[model.Staff]):
    def __init__(self):
        super().__init__(model.Staff)

    async def create(self, obj: schema.IStaffIn) -> model.Staff:
        for k, _ in obj.dict().items():
            if not hasattr(self.model, k):
                obj.dict().pop(k, None)
        new_password = model.Staff.generate_hash(obj.password.get_secret_value())
        new_staff = dict(**obj.dict(exclude={"password"}), password=new_password)
        return await super().create(new_staff)

    async def update(
        self, staff: model.Staff, obj: t.Union[schema.IStaffIn, dict]
    ) -> model.Staff:
        if staff:
            if isinstance(obj, schema.IStaffIn):
                for k, v in obj.dict().items():
                    if hasattr(staff, k):
                        setattr(staff, k, v)
                if obj.password:
                    staff.password = staff.generate_hash(obj.password)
            elif isinstance(obj, dict):
                for k, v in obj.items():
                    if hasattr(staff, k):
                        setattr(staff, k, v)
                if obj.get("passwords", None):
                    staff.password = staff.generate_hash(obj.get("passwords"))
        self.db.add(staff)
        await self.db.commit()
        return staff

    async def add_staff_permissions(
        self,
        staff_id: str,
        permission_objs: t.List[Permission],
    ) -> model.Staff:
        staff = await super().get(staff_id, load_related=True, expunge=False)
        if staff is None:
            raise NotFoundError("staff not found")
        existed_permissions = set()
        for permission in permission_objs:
            for perm in staff.permissions:
                if perm.name == permission.name:
                    existed_permissions.add(permission.name)
        if len(existed_permissions) > 0:
            raise DuplicateError(
                f"`{','.join(existed_permissions)}`roles already exists for staff {staff.firstname} {staff.lastname}"
            )

        staff.permissions.extend(permission_objs)
        self.db.add(staff)
        await self.db.commit()
        await self.db.refresh(staff)
        return staff

    async def remove_staff_permission(
        self,
        staff_id: str,
        permission_objs: t.List[Permission],
    ) -> model.Staff:
        staff = await super().get(staff_id, load_related=True, expunge=False)
        if staff is None:
            raise NotFoundError("staff not found")
        if len(staff.permissions) == 0:
            raise NotFoundError("staff has no permissions")
        for permission in permission_objs:
            for perm in staff.permissions:
                if not perm.name == permission.name:
                    raise DuplicateError(
                        f"Permission `{permission.name }` not found for staff {staff.firstname} {staff.lastname}"
                    )

                staff.permissions.remove(perm)
        self.db.add(staff)
        await self.db.commit()
        await self.db.refresh(staff)
        return staff

    async def get_by_email(self, email: str) -> model.Staff:
        staff = await super().get_by_attr(attr=dict(email=email), first=True)
        return staff

    async def update_password(
        self, staff: model.Staff, obj: schema.IStaffResetPassword
    ) -> model.Staff:
        str_pass = obj.password.get_secret_value()
        staff.password = staff.generate_hash(str_pass)
        self.db.add(staff)
        await self.db.commit()
        return staff

    async def activate(self, staff: model.Staff, mode: bool = True) -> model.Staff:
        staff.is_active = mode
        staff.is_verified = mode
        staff.is_suspended = mode
        self.db.add(staff)
        await self.db.commit()
        return staff

    async def delete(self, staff: model.Staff, permanent: bool = False) -> model.Staff:
        if permanent:
            await super().delete(staff.id)
            return True
        return await self.activate(staff, mode=permanent)


staff_query = StaffQuery()
