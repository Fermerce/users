import os

from core.settings import config
from lib.errors import error
from lib.utils import os_operation


def iter_media(file_path: str, content_type: str) -> object:
    path = f"{config.media_file_dir}/{file_path}"
    if content_type.split("/")[1] == "pdf":
        path = f"{config.pdf_media_file_dir}/{file_path}"
    if not os_operation.check_dir(path):
        raise error.NotFoundError(f"Unsupported media type {content_type}")
    file_size = os.path.getsize(path)
    default_chunk_size = 1024
    if file_size > (default_chunk_size * 10):
        chunk_size = default_chunk_size * 1024  # 1 MB
    else:
        chunk_size = default_chunk_size
    with open(path, mode="rb", buffering=chunk_size) as file_obj:
        yield from file_obj
