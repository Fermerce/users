import typing as t
import fastapi
from core import settings
from core.repository.base import BaseRepository
from src.app.medias import model
from lib.utils import os_operation
from lib.utils.random_string import random_str


class MediaRepository(BaseRepository[model.Media]):
    def __init__(self):
        super().__init__(model.Media)

    @property
    def allowed_image_extensions(self) -> t.List[str]:
        return ["jpg", "png", "jpeg", "gif", "webp"]

    @property
    def allowed_document_extensions(self) -> t.List[str]:
        return ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx"]

    @property
    def allowed_video_extensions(self) -> t.List[str]:
        return ["mp4", "mov", "avi", "wmv", "mkv"]

    @property
    def allowed_audio_extensions(self) -> t.List[str]:
        return ["mp3", "ogg", "wav"]

    @property
    def all_allowed_files(self) -> t.List[str]:
        return [
            *self.allowed_image_extensions,
            *self.allowed_document_extensions,
            *self.allowed_video_extensions,
            *self.allowed_audio_extensions,
        ]

    def convert_image_name_to_url(self, image_url: str, request: fastapi.Request) -> str:
        image_full_url = (
            f"{request.url_for(settings.config.media_url_endpoint_name, uri=image_url)}"
        )
        return image_full_url

    def check_file_type(
        self,
        file_type: t.Union[t.List[str], str] = None,
        media_objs: t.List[fastapi.UploadFile] = [],
    ) -> bool:
        if not media_objs:
            return False
        if not file_type:
            raise ValueError("file_type cannot be empty")
        not_allowed_file_types = [
            media.filename.split(".")[-1]
            for media in media_objs
            if media.content_type.split("/")[-1] not in file_type
        ]
        return bool(not_allowed_file_types)



    def get_file_type(self, content_type: str, to_check: str):
        return content_type.lower().endswith("/" + to_check.lower())

    async def upload_to_db(
        self,
        media_alt_list: t.List[str],
        media_url_list: t.List[str],
        media_type_list: t.List[str],
        media_name_list: t.List[str],
    ) -> t.Union[t.List[model.Media], bool]:
        if not any([media_alt_list, media_url_list, media_type_list]):
            raise ValueError("media_alt_list, media_url_list and media_type_list cannot be empty")
        try:
            media_obj_list = [
                {
                    "name": f"{name}-{random_str(5)}",
                    "alt": alt,
                    "url": url,
                    "content_type": content_type,
                }
                for name, alt, url, content_type in zip(
                    media_name_list, media_alt_list, media_url_list, media_type_list
                )
            ]
            new_media_objects = await super().create_many(media_obj_list)
            return new_media_objects
        except Exception as e:
            raise e

    async def create(
        self,
        media_objs: t.List[fastapi.UploadFile],
        request: fastapi.Request,
    ) -> t.List[model.Media]:
        try:
            if not media_objs:
                raise ValueError("media_objs cannot be empty")
            for media in media_objs:
                if not media:
                    raise ValueError(f"Expected media object, got {type(media)}")

            media_alt_list = []
            media_name_list = []
            media_type_list = []
            media_url_list = []
            for media in media_objs:
                media_type_list.append(media.content_type)
                media_name = os_operation.write_file_to_system(
                    media,
                    settings.config.pdf_media_file_dir
                    if self.get_file_type(media.content_type, "pdf")
                    else settings.config.media_file_dir,
                )

                media_alt_list.append(media_name)
                media_url_list.append(self.convert_image_name_to_url(media_name, request))
                media_name_list.append(media.filename.split(".")[0])

            new_media_list = await self.upload_to_db(
                media_alt_list,
                media_url_list,
                media_type_list,
                media_name_list,
            )
            return new_media_list
        except Exception:
            raise fastapi.HTTPException("Error in creating media", status_code=500)

    async def update(
        self,
        media_obj: fastapi.UploadFile,
        old_media: model.Media,
    ) -> t.List[model.Media]:
        try:
            if media_obj and old_media:
                media_name = os_operation.write_file_to_system(
                    media_obj,
                    settings.config.pdf_media_file_dir
                    if self.get_file_type(old_media.content_type, "pdf")
                    else settings.config.media_file_dir,
                    existing_name=old_media.alt,
                )
                if media_name:
                    old_media.alt = media_name
                    old_media.content_type = media_obj.content_type
                    old_media.url = self.convert_image_name_to_url(media_name, None)
                    updated_media = await self.update_one(old_media.id, old_media.dict())
                    return [updated_media]
                return []
        except Exception:
            raise fastapi.HTTPException("Error in updating media", status_code=500)

    async def delete(self, media_obj: t.List[model.Media], trash: bool = False) -> bool:
        if media_obj:
            if trash:
                for item in media_obj:
                    item.is_active = False
                self.db.add_all(media_obj)
                await self.db.commit()
                return True
            path_list = []
            for item in media_obj:
                delete_type = self.get_file_type(item.content_type, "pdf")
                if delete_type:
                    path = f"{settings.config.pdf_media_file_dir}/{item.alt}"
                    path_list.append(path)
                else:
                    path = f"{settings.config.media_file_dir}/{item.alt}"
                    path_list.append(path)
            os_operation.remove_path(path_list)
            object_id_list = [str(item.id) for item in media_obj]
            result = await super().delete_many(object_id_list)
            if result:
                return True
            else:
                return False
        return None


media_repo = MediaRepository()
