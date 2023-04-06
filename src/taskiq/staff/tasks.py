from datetime import timedelta
from src.app.users.staff.query import staff_query
from src.taskiq.broker import broker
from lib.shared.mail.mailer import Mailer
from lib.utils import security
from core.settings import config


@broker.task
def send_staff_activation_email(staff: dict):
    token: str = security.JWTAUTH.data_encoder(data={"staff_id": str(staff.get("id"))})
    url = f"{config.project_url}/auth/activateAccount?activate_token={token}&auth_type=staff"
    mail_template_context = {
        "url": url,
        "button_label": "confirm",
        "title": "Email confirmation link",
        "description": f"""Hello {staff.get('full_name')}, 
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

    new_mail.send_mail(email=[staff.get("email")])


@broker.task
async def send_staff_password_reset_link(staff: dict):
    staff_id = staff.get("id")
    get_staff = await staff_query.get_by_attr(id=staff_id)
    if get_staff:
        token = security.JWTAUTH.data_encoder(
            data={"staff_id": staff_id}, duration=timedelta(days=1)
        )
        await staff_query.update(staff=get_staff, obj=dict(password_reset_token=token))
        url = f"{config.project_url}/auth/passwordReset?reset_token={token}&auth_type=staff"

        mail_template_context = {
            "url": url,
            "button_label": "reset password",
            "title": "password reset link",
            "description": f"""{staff.get('full_name')} you request for password reset link,
            if not you please contact admin, <br><a href='{url}'>{url}</a>""",
        }
        new_mail = Mailer(
            website_name=config.project_name,
            template_name="action.html",
            context=mail_template_context,
            subject="Password reset link",
        )
        new_mail.send_mail(email=staff.get("email"))


@broker.task
async def send_verify_staff_password_reset(staff: dict):
    staff_id = staff.get("id")
    get_staff = await staff_query.get_by_attr(id=staff_id)
    if get_staff:
        token = security.JWTAUTH.data_encoder(
            data={"staff_id": staff_id}, duration=timedelta(days=1)
        )
        await staff_query.update(staff=get_staff, obj=dict(password_reset_token=token))
        url = f"{config.project_url}/auth/passwordReset?reset_token={token}&auth_type=staff"

        mail_template_context = {
            "url": url,
            "button_label": "reset password",
            "title": "password reset link",
            "description": f"""{staff.get('full_name')} your password was reset successfully,
             if not you please contact admin, <br><a href='{url}'>{url}</a>""",
        }
        new_mail = Mailer(
            website_name=config.project_name,
            template_name="action.html",
            context=mail_template_context,
            subject="Password reset link",
        )
        new_mail.send_mail(email=staff.get("email"))
