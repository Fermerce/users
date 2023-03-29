from src._taskiq.broker import broker
from src.app.auth.repository import auth_token_repo


@broker.task
async def create_token(
    user_ip: str,
    refresh_token: str,
    access_token: str,
    user_id: str,
    token_id: str = None,
):
    await auth_token_repo.create(
        user_id=user_id,
        user_ip=user_ip,
        refresh_token=refresh_token,
        access_token=access_token,
        token_id=token_id,
    )
