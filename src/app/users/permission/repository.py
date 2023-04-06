from core.repository.base import BaseRepository
from src.app.users.permission import model


class PermissionRepository(BaseRepository[model.Permission,]):
    def __init__(self):
        super().__init__(model.Permission)


permission_repo = PermissionRepository()
