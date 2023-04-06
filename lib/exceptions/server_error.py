import typing as t
from fastapi import HTTPException, status


class ServerError(HTTPException):
    def __init__(
        self,
        detail: t.Any = "Error performing request, please try again",
        headers: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> None:
        super().__init__(
            detail=detail,
            headers=headers,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
