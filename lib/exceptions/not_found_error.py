import typing as t
from fastapi import HTTPException, status


class NotFoundError(HTTPException):
    def __init__(
        self,
        detail: t.Any = "data not found",
        headers: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> None:
        super().__init__(
            detail=detail,
            headers=headers,
            status_code=status.HTTP_404_NOT_FOUND,
        )
