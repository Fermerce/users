from datetime import timedelta
from src.app.users.user.repository import users_repo
from src.taskiq.broker import broker
from lib.shared.mail.mailer import Mailer
from lib.utils import security
from core.settings import config


@broker.task(delay=2, priority=1)
def send_users_activation_email(user: dict):
    token: str = security.JWTAUTH.data_encoder(data={"user_id": str(user.get("id"))})
    url = f"{config.project_url}/auth/activateAccount?activate_token={token}&auth_type= user"
    mail_template_context = {
        "url": url,
        "button_label": "confirm",
        "title": "Email confirmation link",
        "description": f"""Hello { user.get('full_name')},
        Welcome to <b>{config.project_name}</b>,
            kindly click on the link below to activate your account
            <b> <a href='{url}'>{url}</a>""",
    }

    new_mail = Mailer(
        website_name=config.project_name,
        template_name="action.html",
        subject="Email confirmation",
        context=mail_template_context,
    )

    new_mail.send_mail(email=[user.get("email")])


@broker.task(delay=2)
def send_email_verification_email(user: dict):
    token: str = security.JWTAUTH.data_encoder(data={"user_id": str(user.get("id"))})
    url = f"{config.project_url}/auth/activateAccount?activate_token={token}&auth_type= user"
    mail_template_context = {
        "url": url,
        "button_label": "confirm email",
        "title": "Email confirmation link",
        "description": f"""Hello { user.get('full_name')},
            kindly click on the link below to confirm your email
            <b> <a href='{url}'>{url}</a>""",
    }

    new_mail = Mailer(
        website_name=config.project_name,
        template_name="action.html",
        subject="Email confirmation",
        context=mail_template_context,
    )

    new_mail.send_mail(email=[user.get("email")])


@broker.task(delay=2, priority=1)
async def send_users_password_reset_link(user: dict):
    user_id = user.get("id")
    get_user = await users_repo.get(id=user_id)
    if get_user:
        token = security.JWTAUTH.data_encoder(
            data={"user_id": user_id}, duration=timedelta(days=1)
        )
        users_repo.update(user=get_user, obj={"reset_token": token})
        url = f"{config.project_url}/auth/passwordReset?reset_token={token}&auth_type= user"

        mail_template_context = {
            "url": url,
            "button_label": "reset password",
            "title": "password reset link",
            "description": f"""{ user.get('full_name')} you request for password reset link,
            if not you please contact admin, <br><a href='{url}'>{url}</a>""",
        }
        new_mail = Mailer(
            website_name=config.project_name,
            template_name="action.html",
            context=mail_template_context,
            subject="Password reset link",
        )
        new_mail.send_mail(email=user.get("email"))


@broker.task(delay=2)
async def send_verify_users_password_reset(user: dict):
    user_id = user.get("id")
    get_user = await users_repo.get(id=user_id)
    if get_user:
        token = security.JWTAUTH.data_encoder(
            data={"user_id": user_id}, duration=timedelta(days=1)
        )
        await users_repo.update(user=get_user, obj=dict(password_reset_token=token))
        url = f"{config.project_url}/auth/passwordReset?reset_token={token}&auth_type= user"

        mail_template_context = {
            "url": url,
            "button_label": "reset password",
            "title": "password reset link",
            "description": f"""{ user.get('full_name')} we notice someone try to change your details,
             if not you click on the link below to reset you password
             <br><a href='{url}'>{url}</a>""",
        }
        new_mail = Mailer(
            website_name=config.project_name,
            template_name="action.html",
            context=mail_template_context,
            subject="Password reset link",
        )
        new_mail.send_mail(email=user.get("email"))
