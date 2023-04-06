from src.taskiq.broker import broker
from src.app.users.auth.query import auth_token_query


@broker.task(delay=1, priority=4)
async def create_token(
    user_ip: str,
    refresh_token: str,
    access_token: str,
    user_id: str,
    token_id: str = None,
):
    await auth_token_query.create_obj(
        user_id=user_id,
        user_ip=user_ip,
        refresh_token=refresh_token,
        access_token=access_token,
        token_id=token_id,
    )
