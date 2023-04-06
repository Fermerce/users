import typing as t
from fastapi import HTTPException, status


class InvalidParameterError(HTTPException):
    def __init__(
        self,
        detail: t.Any = "Invalid parameter",
        headers: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> None:
        super().__init__(
            detail=detail,
            headers=headers,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
