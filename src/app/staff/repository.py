import typing as t
from src._base.repository.base import BaseRepository
from src.app.permission.model import Permission
from src.lib.errors import error
from src.app.staff import model, schema


class StaffRepository(BaseRepository[model.Staff]):
    def __init__(self):
        super().__init__(model.Staff)

    async def create(self, obj: schema.IStaffIn) -> model.Staff:
        for k, _ in obj.dict().items():
            if not hasattr(self.model, k):
                obj.dict().pop(k, None)
        new_password = model.Staff.generate_hash(obj.password.get_secret_value())
        new_staff = dict(**obj.dict(exclude={"password"}), password=new_password)
        return await super().create(new_staff)

    async def update(self, staff: model.Staff, obj: schema.IStaffIn) -> model.Staff:
        if staff:
            for k, v in obj.dict().items():
                if hasattr(staff, k):
                    setattr(staff, k, v)
        if obj.password:
            staff.hash_password()
        self.db.add(staff)
        await self.db.commit()
        return staff

    async def add_staff_permissions(
        self,
        staff_id: str,
        permission_objs: t.List[Permission],
    ) -> model.Staff:
        staff = await super().get(staff_id, load_related=True)
        if staff is None:
            raise error.NotFoundError("staff not found")
        existed_roles = set()
        for permission in permission_objs:
            for perm in staff.permissions:
                if perm.name == permission.name:
                    existed_roles.add(permission.name)
        if len(existed_roles) > 0:
            raise error.DuplicateError(
                f"`{','.join(existed_roles)}`roles already exists for staff {staff.firstname} {staff.lastname}"
            )
        self.db.expunge(staff)

        staff.roles.extend(permission_objs)
        self.db.add(staff)
        await self.db.commit()
        await self.db.refresh(staff)
        return staff

    async def remove_staff_permission(
        self,
        staff: model.Staff,
        permission_objs: t.List[Permission],
    ) -> model.Staff:
        if len(staff.roles) == 0:
            raise error.NotFoundError("staff has no roles")
        for permission in permission_objs:
            for perm in staff.roles:
                if not perm.name == permission.name:
                    raise error.DuplicateError(
                        f"Permission `{permission.name }` not found for staff {staff.firstname} {staff.lastname}"
                    )
                staff.roles.remove(permission)
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
        staff.password = obj.password.get_secret_value()
        staff.hash_password()
        self.db.add(staff)
        await self.db.commit()
        return staff

    async def activate(self, staff: model.Staff, mode: bool = True) -> model.Staff:
        staff.is_active = mode
        self.db.add(staff)
        await self.db.commit()
        return staff

    async def delete(self, staff: model.Staff, permanent: bool = False) -> model.Staff:
        if permanent:
            await super().delete(staff.id)
            return True
        return await self.activate(staff)


staff_repo = StaffRepository()
