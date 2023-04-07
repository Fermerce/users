from fastapi import Request
from core.repository.base import BaseRepository
from src.app.auth import model


class AuthTokeRepository(BaseRepository[model.AuthToken]):
    def __init__(self):
        super().__init__(model.AuthToken)

    async def create(
        self,
        user_id: str,
        user_ip: str,
        access_token: str,
        refresh_token: str,
        return_token: bool = False,
        token_id: str = None,
    ) -> model.AuthToken:
        if token_id:
            result = await super().update(
                token_id,
                dict(
                    access_token=access_token,
                    refresh_token=refresh_token,
                ),
            )
            if return_token:
                return result
            return
        new_auth_token = await super().create(
            dict(
                access_token=access_token,
                refresh_token=refresh_token,
                ip_address=user_ip,
                user_id=user_id,
            )
        )
        if new_auth_token and return_token:
            return new_auth_token

    def get_user_ip(self, request: Request) -> str:
        forwarded_for = request.headers.get("X-Forwarded-For")
        real_ip = request.headers.get("X-Real-IP")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0]
        elif real_ip:
            client_ip = real_ip
        else:
            client_ip = request.client.host
        return client_ip

    async def get_by_ip(self, ip_address: str) -> model.AuthToken:
        return await super().get_by_attr(attr=dict(ip_address=ip_address), first=True)


auth_token_repo = AuthTokeRepository()
