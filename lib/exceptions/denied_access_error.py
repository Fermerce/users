import typing as t
from fastapi import HTTPException, status


class AccessDenied(HTTPException):
    def __init__(
        self,
        detail: t.Any = "Sorry, you do not have the necessary permissions to access this resource",
        headers: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> None:
        super().__init__(
            detail=detail,
            headers=headers,
            status_code=status.HTTP_403_FORBIDDEN,
        )
