import typing as t
from pydantic import BaseModel


class IHealthCheck(BaseModel):
    name: str
    version: str
    description: str


class ITotalCount(BaseModel):
    count: int


class IResponseMessage(BaseModel):
    message: str


class IBaseResponse(BaseModel):
    status: int = 200
    data: t.Union[t.Dict, t.List, t.Tuple, t.AnyStr]
    error: t.Union[t.Dict, t.List, t.Tuple, t.AnyStr]
