import typing as t
from fastapi import APIRouter, Form, Query, Request, UploadFile
from fastapi.responses import StreamingResponse, FileResponse
from src.app.medias import schema, service
from core.settings import config
from core.enum.sort_type import SortOrder


router = APIRouter(
    prefix="/static",
    tags=["static"],
    # include_in_schema=False,
)


@router.post("/")
async def create_resource(request: Request, files: t.List[UploadFile] = Form()):
    return await service.create(request=request, media_objs=files)


@router.put("/{uri}")
async def update_resource(uri: str, file: UploadFile = Form()):
    return await service.update(uri=uri, media_obj=file)


@router.get("/")
async def search_resource(
    filter: t.Optional[str] = Query(
        default="", alias="filter", description="filter all address"
    ),
    select: t.Optional[str] = Query(
        default="", alias="select", description="specific attributes of the permissions"
    ),
    per_page: int = 10,
    page: int = 1,
    sort_by: t.Optional[SortOrder] = Query(
        default=SortOrder.desc, description="order by attribute, e.g. id"
    ),
    order_by: t.Optional[str] = Query(
        default="id", description="order by attribute, e.g. id"
    ),
    is_active: t.Optional[bool] = True,
):
    return await service.filter(
        filter=filter,
        per_page=per_page,
        page=page,
        select=select,
        sort_by=sort_by,
        order_by=order_by,
        is_active=is_active,
    )


@router.get("/{uri}", name=config.media_url_endpoint_name)
async def get_resource(uri: str) -> StreamingResponse:
    return await service.get(uri)


@router.get("/{uri}/download")
async def download_resource(uri: str) -> FileResponse:
    return await service.download(uri)


@router.delete("/{uri}")
async def delete_one_resource(uri: str) -> None:
    return await service.delete_one(uri)


@router.delete("/")
async def delete_many_resource(data_in: schema.IMediaDeleteIn) -> None:
    return await service.delete_many(data_in)
