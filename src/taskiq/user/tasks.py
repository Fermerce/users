from datetime import timedelta
from src.taskiq.broker import broker
from src.lib.shared.mail.mailer import Mailer
from src.lib.utils import security
from src._base.settings import config


@broker.task
def send_activation_email(customer: dict):
    token: str = security.JWTAUTH.data_encoder(data={"id": str(customer.get("id"))})
    url = f"{config.project_url}/auth/activateAccount?activate_token={token}&auth_type=customer"
    mail_template_context = {
        "url": url,
        "button_label": "confirm",
        "title": "Email confirmation link",
        "description": f""" Hello {customer.get('full_name')}, 
        Welcome to <b>{config.project_name}</b>,
            kindly click on the link below to activate your account <br><a href={url}>{url}</a></br>""",
    }

    new_mail = Mailer(
        website_name=config.project_name,
        template_name="action.html",
        subject="Email confirmation",
        context=mail_template_context,
    )

    new_mail.send_mail(email=[customer.get("email")])


@broker.task
def send_password_reset_link(customer: dict):
    token = security.JWTAUTH.data_encoder(
        data={"id": str(customer.get("id"))},
        duration=timedelta(days=1),
    )
    url = f"{config.project_url}/auth/passwordReset?reset_token={token}&auth_type=customer"
    mail_template_context = {
        "url": url,
        "button_label": "reset password",
        "title": "password reset link",
        "description": f" {customer.get('full_name')} you request for password reset link, if not you please contact admin",
    }
    new_mail = Mailer(
        website_name=config.project_name,
        template_name="action.html",
        context=mail_template_context,
        subject="Password reset link",
    )
    new_mail.send_mail(email=customer.get("email"))
