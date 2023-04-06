import typing as t
from fastapi import HTTPException, status


class BadDataError(HTTPException):
    def __init__(
        self,
        detail: t.Any = "Account has been already verified",
        headers: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> None:
        super().__init__(
            detail=detail,
            headers=headers,
            status_code=status.HTTP_400_BAD_REQUEST,
        )
