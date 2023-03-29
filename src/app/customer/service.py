import typing as t
import uuid
from fastapi import status
from fastapi import Response
from src._base.enum.sort_type import SortOrder
from src._base.schema.response import ITotalCount, IResponseMessage
from src.app.permission.model import Permission
from src.lib.errors import error
from src.app.customer import schema, model
from src.app.customer.repository import customer_repo
from src.app.permission.repository import permission_repo
from src.taskiq.user import tasks
from src.lib.utils import security


async def create(data_in=schema.ICustomerIn):
    check_customer = await customer_repo.get_by_email(email=data_in.email)
    if check_customer:
        raise error.DuplicateError("Customer already exist")
    new_customer = await customer_repo.create(data_in)
    if new_customer:
        await tasks.send_customer_activation_email.kicker().with_labels(delay=5).kiq(
            dict(
                email=new_customer.email,
                id=str(new_customer.id),
                full_name=f"{new_customer.firstname} {new_customer.lastname}",
            )
        )
        return IResponseMessage(
            message="Account was created successfully, please check your email to activate your account"
        )
    raise error.ServerError("Could not create account")


async def filter(
    filter: str = "",
    per_page: int = 10,
    page: int = 0,
    select: str = "",
    sort_by: SortOrder = SortOrder.asc,
    order_by: str = None,
    is_active: bool = False,
) -> t.List[model.Customer]:
    get_customers = await customer_repo.filter(
        filter_string=filter,
        per_page=per_page,
        page=page,
        select_columns=select,
        order_by=order_by,
        sort_by=sort_by,
        strict_search=dict(is_active=is_active),
    )
    return get_customers


async def verify_customer_email(
    data_in: schema.ICustomerAccountVerifyToken,
) -> IResponseMessage:
    data: dict = security.JWTAUTH.data_decoder(encoded_data=data_in.token)
    if not data.get("user_id", None):
        raise error.BadDataError("Invalid token data")
    customer_obj = await customer_repo.get(data.get("user_id", None))
    if not customer_obj:
        raise error.BadDataError("Invalid token")

    if customer_obj and customer_obj.is_verified:
        raise error.BadDataError(
            detail="Account has been already verified",
        )
    customer_obj = await customer_repo.activate(customer_obj)
    if customer_obj:
        return IResponseMessage(message="Account was verified successfully")
    raise error.ServerError("Could not activate account, please try again")


async def reset_password_link(
    data_in: schema.IGetPasswordResetLink,
) -> IResponseMessage:
    customer_obj = await customer_repo.get_by_email(email=data_in.email)
    if not customer_obj.is_verified:
        await tasks.send_customer_activation_email.kicker().with_labels(delay=2).kiq(
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
        raise error.NotFoundError("Customer not found")
    await tasks.send_customer_password_reset_link.kicker().with_labels(delay=2).kiq(
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
    if token_data:
        customer_obj = await customer_repo.get(token_data.get("user_id", None))
        if not customer_obj:
            raise error.NotFoundError("Customer not found")
        if customer_obj.password_reset_token != data_in.token:
            raise error.UnauthorizedError()
        if customer_obj.check_password(data_in.password.get_secret_value()):
            raise error.BadDataError("Try another password you have not used before")
        if await customer_repo.update_password(customer_obj, data_in):
            await tasks.send_verify_customer_password_reset.kicker().with_labels(
                delay=2
            ).kiq(
                dict(
                    email=customer_obj.email,
                    id=str(customer_obj.id),
                    full_name=f"{customer_obj.firstname} {customer_obj.lastname}",
                )
            )
            return IResponseMessage(message="password was reset successfully")
    raise error.BadDataError("Invalid token was provided")


async def update_customer_password_no_token(
    data_in: schema.ICustomerResetPassword, user_data: model.Customer
) -> IResponseMessage:
    customer_obj = await customer_repo.get(user_data.id)
    if not customer_obj:
        raise error.NotFoundError("Customer not found")

    if customer_obj.check_password(data_in.password.get_secret_value()):
        raise error.BadDataError("Try another password you have not used before")
    if await customer_repo.update_password(customer_obj, data_in):
        await tasks.send_customer_password_reset_link.kicker().with_labels(delay=2).kiq(
            dict(
                email=customer_obj.email,
                id=str(customer_obj.id),
                full_name=f"{customer_obj.firstname} {customer_obj.lastname}",
            )
        )
        return IResponseMessage(message="password was reset successfully")
    raise error.BadDataError("Invalid token was provided")


async def remove_customer_data(data_in: schema.ICustomerRemove) -> None:
    customer_to_remove = await customer_repo.get(data_in.customer_id)
    if customer_to_remove:
        await customer_repo.delete(
            customer=customer_to_remove, permanent=data_in.permanent
        )
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise error.NotFoundError(
        f"Customer with customer id {data_in.customer_id} does not exist"
    )


async def get_customers(
    limit: int,
    offset: int,
    filter: str,
    select: str,
) -> t.List[model.Customer]:
    customers = await customer_repo.filter(
        filter_obj=filter,
        offset=offset,
        limit=limit,
        select_list=select,
    )
    return customers


async def get_total_customers():
    total_count = await customer_repo.get_count()
    return ITotalCount(count=total_count).dict()


async def get_customer(
    customer_id: uuid.UUID, load_related: bool = False
) -> model.Customer:
    if not customer_id:
        raise error.NotFoundError(
            f"Customer with customer id {customer_id} does not exist",
        )
    use_detail = await customer_repo.get(customer_id, load_related=load_related)
    if use_detail:
        try:
            if not load_related:
                return schema.ICustomerOut.from_orm(use_detail)
            return schema.ICustomerOutFull.from_orm(use_detail)
        except Exception as e:
            raise error.ServerError("Error getting customer data")
    raise error.NotFoundError(
        f"Customer with customer id {customer_id} does not exist",
    )


async def get_customer_permissions(customer_id: uuid.UUID) -> t.List[Permission]:
    use_detail = await customer_repo.get(customer_id, load_related=True)
    if use_detail:
        return use_detail.permissions
    raise error.NotFoundError(
        f"Customer with customer id {customer_id} does not exist",
    )


async def add_customer_permissions(
    data_in: schema.ICustomerRoleUpdate,
) -> IResponseMessage:
    get_per = await permission_repo.get_by_props(
        prop_name="id", prop_values=data_in.permissions
    )
    if not get_per:
        raise error.NotFoundError("permission not found")
    update_customer = await customer_repo.add_customer_permission(
        customer_id=data_in.customer_id,
        permission_objs=get_per,
    )
    if update_customer:
        return IResponseMessage(message="customer permission was updated successfully")


async def remove_customer_permissions(
    data_in: schema.ICustomerRoleUpdate,
) -> IResponseMessage:
    check_perm = await permission_repo.get_by_ids(data_in.permissions)
    if not check_perm:
        raise error.NotFoundError(detail="Permission not found")
    await customer_repo.remove_customer_permission(
        customer_id=data_in.customer_id, permission_objs=check_perm
    )
    return IResponseMessage(message="Customer permission was updated successfully")
