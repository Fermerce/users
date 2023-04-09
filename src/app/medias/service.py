import os
import typing as t
from core.enum.sort_type import SortOrder
from core.schema.response import ResponseMessage
from lib.errors import error
from fastapi import Request, UploadFile, status
from fastapi.responses import (
    FileResponse,
    StreamingResponse,
)
from src.app.medias import model, schema, validator, util
from src.app.medias.repository import media_repo

from core.settings import config
from lib.utils import os_operation


async def create(request: Request, media_objs: t.Optional[t.List[UploadFile]]):
    try:
        oversized_files = validator.check_file_size(media_objs)
        if oversized_files:
            raise error.BadDataError(
                f"The following files are too large: {','.join(oversized_files)}"
            )
        bad_types = media_repo.check_file_type(
            file_type=media_repo.all_allowed_files, media_objs=media_objs
        )
        if bad_types:
            raise error.BadDataError("Unsupported media type, expected")
        await media_repo.create(media_objs=media_objs, request=request)
        return ResponseMessage(message="Resource created successfully")
    except Exception:
        raise error.ServerError("Error while creating resource")


async def update(uri: str, media_obj: UploadFile) -> ResponseMessage:
    try:
        bad_types = media_repo.check_file_type(
            file_type=media_repo.all_allowed_files,
            media_objs=[media_obj],
        )
        if bad_types:
            raise error.BadDataError("Unsupported media type")
        oversized_files = validator.check_file_size([media_obj])
        if oversized_files:
            raise error.BadDataError(f"file is too large: {','.join(oversized_files)}")
        get_media = await media_repo.get_by_attr(attr=dict(alt=uri), first=True)
        if not get_media:
            raise error.NotFoundError(f"Resource with URI {uri} not found")
        expected_extension = get_media.alt.split(".")[-1]
        actual_extension = media_obj.content_type.split("/")[1]
        if expected_extension != actual_extension:
            raise error.BadDataError(
                f"Invalid file extension. Expected {expected_extension} but got {actual_extension}."
            )
        result = await media_repo.update(media_obj=media_obj, old_media=get_media)
        if result:
            return ResponseMessage(message="Resource updated successfully")
    except Exception:
        raise error.ServerError(
            f"Error while updating resource with URI {uri}. Make sure you are uploading a valid file."
        )


async def get(uri: str) -> StreamingResponse:
    try:
        check_file = await media_repo.get_by_attr(attr=dict(alt=uri), first=True)
        if not check_file:
            raise error.NotFoundError("Resource Not found")
        return StreamingResponse(
            util.iter_media(
                file_path=check_file.alt,
                content_type=check_file.content_type,
            ),
            media_type=check_file.content_type,
        )
    except Exception:
        raise error.ServerError("Error while retrieving resource")


async def filter(
    filter: str,
    per_page: int = 10,
    page: int = 0,
    select: str = "",
    sort_by: SortOrder = SortOrder.asc,
    order_by: str = None,
    is_active: bool = True,
) -> t.List[model.Media]:
    get_medias = await media_repo.filter(
        filter_string=filter,
        per_page=per_page,
        page=page,
        select_columns=select,
        sort_by=sort_by,
        order_by=order_by,
        strict_search=dict(is_active=is_active),
    )
    return get_medias


async def download(
    uri: str,
) -> FileResponse:
    check_file = await media_repo.get_by_attr(attr=dict(alt=uri), first=True)
    if not check_file:
        raise error.NotFoundError("Resource Not found")
    path = None
    if check_file.content_type.split("/")[0] == "image":
        path = f"{config.media_file_dir}/{check_file.alt}"
    elif check_file.content_type.split("/")[1] == "pdf":
        path = f"{config.pdf_media_file_dir}/{check_file.alt}"
    else:
        raise error.NotFoundError("Resource Not found")
    return FileResponse(
        path,
        status_code=status.HTTP_200_OK,
        filename=uri,
    )


async def delete_many(data_in: schema.IMediaDeleteIn) -> ResponseMessage:
    check_file = await media_repo.get_by_props(
        prop_name="alt", prop_values=data_in.uris
    )
    if check_file:
        await media_repo.delete(media_obj=check_file, trash=data_in.trash)
        return ResponseMessage(message="Resource deleted successfully")
    raise error.NotFoundError("Resource Not found")


async def delete_one(
    uri: str,
    trash: bool = False,
) -> ResponseMessage:
    check_file = await media_repo.get_by_props(prop_name="alt", prop_values=[uri])
    if check_file:
        await media_repo.delete(media_obj=[check_file], trash=trash)
        return ResponseMessage(message="Resource deleted successfully")
    raise error.NotFoundError("Resource Not found")
