from datetime import timedelta
import dramatiq
from src.lib.shared.mail.mailer import Mailer
from src.lib.utils import security
from src._base.settings import config


@dramatiq.actor
def send_activation_email(customer: dict):
    token: str = security.JWTAUTH.data_encoder(data={"id": str(customer.get("id"))})
    mail_template_context = {
        "url": f"{config.project_url}/auth/activateAccount?activate_token={token}",
        "button_label": "confirm",
        "title": "Email confirmation link",
        "description": f"""Welcome to <b>{config.project_name}</b>,
            kindly click on the link below to activate your account""",
    }

    new_mail = Mailer(
        website_name=config.project_name,
        template_name="action.html",
        subject="Email confirmation",
        context=mail_template_context,
    )

    new_mail.send_mail(email=[customer.get("email")])


@dramatiq.actor
def send_password_reset_link(customer: dict):
    token = security.JWTAUTH.data_encoder(
        data={"id": str(customer.get("id"))},
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
    new_mail.send_mail(email=customer.get("email"))
