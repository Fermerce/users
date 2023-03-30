from datetime import timedelta
from src.app.customer.repository import customer_repo
from src._taskiq.broker import broker
from src.lib.shared.mail.mailer import Mailer
from src.lib.utils import security
from src._base.settings import config


@broker.task(delay=2, priority=1)
def send_customer_activation_email(customer: dict):
    token: str = security.JWTAUTH.data_encoder(
        data={"user_id": str(customer.get("id"))}
    )
    url = f"{config.project_url}/auth/activateAccount?activate_token={token}&auth_type=customer"
    mail_template_context = {
        "url": url,
        "button_label": "confirm",
        "title": "Email confirmation link",
        "description": f"""Hello {customer.get('full_name')}, 
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

    new_mail.send_mail(email=[customer.get("email")])


@broker.task(delay=2)
def send_email_verification_email(customer: dict):
    token: str = security.JWTAUTH.data_encoder(
        data={"user_id": str(customer.get("id"))}
    )
    url = f"{config.project_url}/auth/activateAccount?activate_token={token}&auth_type=customer"
    mail_template_context = {
        "url": url,
        "button_label": "confirm email",
        "title": "Email confirmation link",
        "description": f"""Hello {customer.get('full_name')},
            kindly click on the link below to confirm your email
            <b> <a href='{url}'>{url}</a>""",
    }

    new_mail = Mailer(
        website_name=config.project_name,
        template_name="action.html",
        subject="Email confirmation",
        context=mail_template_context,
    )

    new_mail.send_mail(email=[customer.get("email")])


@broker.task(delay=2, priority=1)
async def send_customer_password_reset_link(customer: dict):
    user_id = customer.get("id")
    get_user = await customer_repo.get(id=user_id)
    if get_user:
        token = security.JWTAUTH.data_encoder(
            data={"user_id": user_id}, duration=timedelta(days=1)
        )
        customer_repo.update(customer=get_user, obj={"password_reset_token": token})
        url = f"{config.project_url}/auth/passwordReset?reset_token={token}&auth_type=customer"

        mail_template_context = {
            "url": url,
            "button_label": "reset password",
            "title": "password reset link",
            "description": f"""{customer.get('full_name')} you request for password reset link,
            if not you please contact admin, <br><a href='{url}'>{url}</a>""",
        }
        new_mail = Mailer(
            website_name=config.project_name,
            template_name="action.html",
            context=mail_template_context,
            subject="Password reset link",
        )
        new_mail.send_mail(email=customer.get("email"))


@broker.task(delay=2)
async def send_verify_customer_password_reset(customer: dict):
    user_id = customer.get("id")
    get_user = await customer_repo.get(id=user_id)
    if get_user:
        token = security.JWTAUTH.data_encoder(
            data={"user_id": user_id}, duration=timedelta(days=1)
        )
        await customer_repo.update(
            customer=get_user, obj=dict(password_reset_token=token)
        )
        url = f"{config.project_url}/auth/passwordReset?reset_token={token}&auth_type=customer"

        mail_template_context = {
            "url": url,
            "button_label": "reset password",
            "title": "password reset link",
            "description": f"""{customer.get('full_name')} we notice someone try to change your details , 
             if not you click on the link below to reset you password
             <br><a href='{url}'>{url}</a>""",
        }
        new_mail = Mailer(
            website_name=config.project_name,
            template_name="action.html",
            context=mail_template_context,
            subject="Password reset link",
        )
        new_mail.send_mail(email=customer.get("email"))
