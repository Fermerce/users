from src._base.repository.base import BaseRepository
from src.app.permission import model


class PermissionRepository(BaseRepository[model.Permission,]):
    def __init__(self):
        super().__init__(model.Permission)


permission_repo = PermissionRepository()
