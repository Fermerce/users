import typing as t
from src._base.repository.base import BaseRepository
from src.app.permission.model import Permission
from src.lib.errors import error
from src.app.customer import model, schema


class CustomerRepository(BaseRepository[model.Customer]):
    def __init__(self):
        super().__init__(model.Customer)

    async def create(self, obj: schema.ICustomerIn) -> model.Customer:
        for k, _ in obj.dict().items():
            if not hasattr(self.model, k):
                obj.dict().pop(k, None)
        new_password = model.Customer.generate_hash(obj.password.get_secret_value())
        new_customer = dict(**obj.dict(exclude={"password"}), password=new_password)

        return await super().create(new_customer)

    async def update(
        self, customer: model.Customer, obj: t.Union[schema.ICustomerIn, dict]
    ) -> model.Customer:
        if customer:
            if isinstance(obj, schema.ICustomerIn):
                for k, v in obj.dict().items():
                    if hasattr(customer, k):
                        setattr(customer, k, v)
                if obj.password:
                    customer.password = customer.generate_hash(obj.get("password"))
            elif isinstance(obj, dict):
                for k, v in obj.items():
                    if hasattr(customer, k):
                        setattr(customer, k, v)
                if obj.get("password", None):
                    customer.password = customer.generate_hash(obj.get("password"))
        self.db.add(customer)
        await self.db.commit()
        return customer

    async def add_customer_permission(
        self,
        customer_id: str,
        permission_objs: t.List[Permission],
    ) -> model.Customer:
        customer = await super().get(customer_id, load_related=True, expunge=True)
        if customer is None:
            raise error.NotFoundError("customer not found")
        existed_perms = set()
        for permission in permission_objs:
            for per in customer.permissions:
                if per.name == permission.name:
                    existed_perms.add(permission.name)
                    permission_objs.pop(permission_objs.index(permission))
        if len(existed_perms) > 0:
            raise error.DuplicateError(
                f"`{','.join(existed_perms)}`role/roles already exists"
            )

        customer.permissions.extend(permission_objs)
        self.db.add(customer)
        await self.db.commit()
        await self.db.refresh(customer)
        return customer

    async def remove_customer_permission(
        self,
        customer_id: str,
        permission_objs: t.List[Permission],
    ) -> model.Customer:
        customer = await super().get(customer_id, load_related=True, expunge=False)
        if customer is None:
            raise error.NotFoundError("customer not found")
        if len(customer.permissions) == 0:
            raise error.NotFoundError("customer has no permissions")
        for permission in permission_objs:
            for per in customer.permissions:
                if not per.name == permission.name:
                    raise error.DuplicateError(
                        f"role `{permission.name }` not found for customer {customer.firstname} {customer.lastname}"
                    )
            customer.permissions.remove(per)
        self.db.add(customer)
        await self.db.commit()
        await self.db.refresh(customer)
        return customer

    async def get_by_email(self, email: str) -> model.Customer:
        customer = await super().get_by_attr(attr=dict(email=email), first=True)
        return customer

    async def update_password(
        self, customer: model.Customer, obj: schema.ICustomerResetPassword
    ) -> model.Customer:
        str_pass = obj.password.get_secret_value()
        customer.password = customer.generate_hash(str_pass)
        self.db.add(customer)
        await self.db.commit()
        return customer

    async def activate(
        self, customer: model.Customer, mode: bool = True
    ) -> model.Customer:
        customer.is_active = mode
        customer.is_verified = mode
        customer.is_suspended = mode
        self.db.add(customer)
        await self.db.commit()
        return customer

    async def delete(
        self, customer: model.Customer, permanent: bool = False
    ) -> model.Customer:
        if permanent:
            await super().delete(id=str(customer.id))
            return True
        return await self.activate(customer, mode=permanent)


customer_repo = CustomerRepository()
