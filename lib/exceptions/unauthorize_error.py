import typing as t
from fastapi import HTTPException, status


class UnauthorizedError(HTTPException):
    def __init__(
        self,
        detail: t.Any = "Authentication failed",
        headers: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> None:
        super().__init__(
            detail=detail,
            headers=headers,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
