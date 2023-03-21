import typing as t
from datetime import timedelta
import uuid
from fastapi import status
from fastapi import BackgroundTasks, Response
from src.app.permission.model import Permission
from src.lib.base.enum.sort_type import SortOrder
from src.lib.base.schema.response import ITotalCount, ResponseMessage
from src.lib.errors import error
from src.lib.base.settings import config
from src.app.user import schema, model
from src.app.user.repository import user_repo
from src.app.permission.repository import permission_repo
from src.lib.shared.mail.mailer import Mailer
from src.lib.utils import security


async def create(
    background_tasks: BackgroundTasks,
    data_in=schema.IRegister,
):
    check_user = await user_repo.get_by_email(data_in.email)
    if check_user:
        raise error.DuplicateError("User already exist")
    new_user = await user_repo.create(data_in)
    token: str = security.JWTAUTH.data_encoder(data={"user_id": str(new_user.id)})
    mail_template_context = {
        "url": f"{config.project_url}/auth/activateAccount?activate_token={token}",
        "button_label": "confirm",
        "title": "user email confirmation link",
        "description": f"""Welcome to <b>{config.project_name}</b>,
            kindly click on the link below to activate your account""",
    }

    new_mail = Mailer(
        website_name=config.project_name,
        template_name="action.html",
        subject="Email confirmation",
        context=mail_template_context,
    )
    background_tasks.add_task(new_mail.send_mail, email=[new_user.email])
    return ResponseMessage(
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
) -> t.List[model.User]:
    get_users = await user_repo.filter(
        filter_string=filter,
        per_page=per_page,
        page=page,
        select_columns=select,
        order_by=order_by,
        sort_by=sort_by,
        strict_search=dict(is_active=is_active),
    )
    return get_users


async def verify_user_email(
    user_token: schema.IUserAccountVerifyToken,
) -> ResponseMessage:
    data: dict = security.JWTAUTH.data_decoder(encoded_data=user_token.token)
    if not data.get("user_id", None):
        raise error.BadDataError("Invalid token data")
    user_obj = await user_repo.get(data.get("user_id", None))
    if user_obj and user_obj.is_active:
        raise error.BadDataError(
            detail="Account has been already verified",
        )
    user_obj = await user_repo.activate(user_obj)
    if user_obj:
        return ResponseMessage(message="Account was verified successfully")


async def reset_password_link(
    background_task: BackgroundTasks,
    user_data: schema.IGetPasswordResetLink,
) -> ResponseMessage:
    user_obj = await user_repo.get_by_email(email=user_data.email)
    if not user_obj:
        raise error.NotFoundError("User not found")
    token = security.JWTAUTH.data_encoder(
        data={"user_id": str(user_obj.id)},
        duration=timedelta(days=1),
    )
    mail_template_context = {
        "url": f"{config.project_url}/auth/passwordReset?reset_token={token}",
        "button_label": "reset password",
        "title": "password reset link",
        "description": "You request for password reset link, if not you please contact admin",
    }
    new_mail = Mailer(
        website_name=config.project_name,
        template_name="action.html",
        context=mail_template_context,
        subject="Password reset link",
    )
    background_task.add_task(new_mail.send_mail, email=[user_obj.email])
    return ResponseMessage(
        message="Password reset token has been sent to your email, link expire after 24 hours"
    )


async def update_user_password(
    user_data: schema.IResetPassword,
) -> ResponseMessage:
    token_data: dict = security.JWTAUTH.data_decoder(encoded_data=user_data.token)
    if token_data:
        user_obj = await user_repo.get(token_data.get("user_id", None))
        if not user_obj:
            raise error.NotFoundError("User not found")
        if user_obj.check_password(user_data.password.get_secret_value()):
            raise error.BadDataError("Try another password you have not used before")
        if await user_repo.update_password(user_obj, user_data):
            return ResponseMessage(message="password was reset successfully")
    raise error.BadDataError("Invalid token was provided")


async def get_current_user_data(
    user: model.User,
) -> model.User:
    if not user:
        raise error.NotFoundError("data not found for user")
    return user


async def remove_user_data(user_id: uuid.UUID, permanent: bool = False) -> None:
    user_to_remove = await user_repo.get(user_id)
    if user_to_remove:
        await user_repo.delete(user=user_to_remove, permanent=permanent)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise error.NotFoundError(f"User with user_id {user_id} does not exist")


async def get_users(
    limit: int,
    offset: int,
    filter: str,
    select: str,
) -> t.List[model.User]:
    users = await user_repo.filter(
        filter_obj=filter,
        offset=offset,
        limit=limit,
        select_list=select,
    )
    return users


async def get_total_users():
    total_count = await user_repo.get_count()
    return ITotalCount(count=total_count)


async def get_user(
    user_id: uuid.UUID,
) -> model.User:
    use_detail = await user_repo.get(user_id, load_related=True)
    if use_detail:
        return use_detail
    raise error.NotFoundError(
        f"User with user_id {user_id} does not exist",
    )


async def add_user_role(
    data_in: schema.IUserPermissionUpdate,
    user_id: uuid.UUID,
) -> ResponseMessage:
    get_perms = await permission_repo.get_by_props(
        prop_name="id", prop_values=data_in.permissions
    )
    if not get_perms:
        raise error.NotFoundError("Permission not found")
    update_user = await user_repo.add_user_permission(
        user_id=user_id,
        perm_objs=get_perms,
    )
    if update_user:
        return ResponseMessage(message="User permission was updated successfully")


async def get_user_role(
    user_id: uuid.UUID,
) -> t.List[Permission]:
    check_user = await user_repo.get(user_id, load_related=True)
    if check_user:
        return check_user.permissions
    raise error.NotFoundError("User not found")


async def remove_user_role(
    data_in: schema.IUserPermissionUpdate,
    user_id: uuid.UUID,
) -> None:
    check_perms = await permission_repo.get_by_ids(data_in.permissions)
    if not check_perms:
        raise error.NotFoundError(detail="Permission not found")
    await user_repo.remove_user_permission(user_id=user_id, perm_objs=check_perms)
    return ResponseMessage(message="User role was updated successfully")
