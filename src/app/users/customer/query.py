import typing as t
from core.query.base_query import BaseQuery
from src.app.users.permission.model import Permission
from lib.exceptions.not_found_error import NotFoundError
from lib.exceptions.duplicate_error import DuplicateError
from src.app.users.customer import model, schema


class CustomerQuery(BaseQuery[model.Customer]):
    def __init__(self):
        super().__init__(model.Customer)

    async def create_obj(self, obj: schema.ICustomerIn) -> model.Customer:
        for k, _ in obj.dict().items():
            if not hasattr(self.model, k):
                obj.dict().pop(k, None)
        new_password = model.Customer.generate_hash(obj.password.get_secret_value())
        new_customer = dict(**obj.dict(exclude={"password"}), password=new_password)

        return await super().create_obj(new_customer)

    async def update_obj(
        self, customer: model.Customer, obj: t.Union[schema.ICustomerIn, dict]
    ) -> model.Customer:
        to_update = dict()
        if customer:
            if isinstance(obj, schema.ICustomerIn):
                for k, v in obj.dict().items():
                    if hasattr(customer, k):
                        setattr(to_update, k, v)
                if obj.password:
                    password = customer.generate_hash(obj.password.get_secret_value())
                    setattr(to_update, "password", password)
            elif isinstance(obj, dict):
                for k, v in obj.items():
                    if hasattr(customer, k):
                        setattr(customer, k, v)
                if obj.get("password", None):
                    password = customer.generate_hash(obj.get("password"))
                    setattr(to_update, "password", password)
        customer = await customer.update(**to_update)
        return customer

    async def add_customer_permission(
        self,
        customer_id: str,
        permission_objs: t.List[Permission],
    ) -> model.Customer:
        customer: model.Customer = await super().get_by_attr(
            id=customer_id, load_related=True
        )
        if customer is None:
            raise NotFoundError("customer not found")
        existed_perms = set()

        for permission in permission_objs:
            for per in customer.permissions:
                if per.name == permission.name:
                    existed_perms.add(permission.name)
                    permission_objs.pop(permission_objs.index(permission))
        if len(existed_perms) > 0:
            raise DuplicateError(
                f"`{','.join(existed_perms)}`role/roles already exists"
            )

        await customer.permissions.add(permission_objs)
        return customer

    async def remove_customer_permission(
        self,
        customer_id: str,
        permission_objs: t.List[Permission],
    ) -> model.Customer:
        customer = await super().get_by_attr(customer_id, load_related=True)
        if customer is None:
            raise NotFoundError("customer not found")
        if len(customer.permissions) == 0:
            raise NotFoundError("customer has no permissions")
        for permission in permission_objs:
            for per in customer.permissions:
                if not per.name == permission.name:
                    raise DuplicateError(
                        f"role `{permission.name }` not found for customer {customer.firstname} {customer.lastname}"
                    )
            customer = await customer.permissions.remove(per)

        return customer

    async def update_password(
        self, customer: model.Customer, obj: schema.ICustomerResetPassword
    ) -> model.Customer:
        str_pass = obj.password.get_secret_value()
        password = customer.generate_hash(str_pass)
        await customer.update(password=password)
        return customer

    async def activate(
        self, customer: model.Customer, mode: bool = True
    ) -> model.Customer:
        customer.is_active = mode
        customer.is_verified = mode
        customer.is_suspended = mode
        await customer.upsert()
        return customer

    async def delete(
        self, customer: model.Customer, permanent: bool = False
    ) -> model.Customer:
        if permanent:
            await super().delete_obj(id=str(customer.id))
            return True
        return await self.activate(customer, mode=permanent)


customer_query = CustomerQuery()
