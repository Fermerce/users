from fastapi import UploadFile
import typing as t


def check_file_size(
    files: t.List[UploadFile], max_size: int = 5 * 1024 * 1024  # 5 MB by default
) -> t.List[str]:
    """Checks if any of the uploaded files exceed the specified size limit.

    Args:
        files (List[UploadFile]): List of uploaded files.
        max_size (int, optional): Maximum allowed file size in bytes. Defaults to 5 MB.

    Returns:
        List[str]: List of filenames that exceed the size limit.
    """
    oversized_files = []
    for file in files:
        if file.size > max_size:
            oversized_files.append(file.filename)
    return oversized_files
