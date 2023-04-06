from core.query.base_query import BaseQuery
from src.app.users.permission import model


class PermissionQuery(BaseQuery[model.Permission,]):
    def __init__(self):
        super().__init__(model.Permission)

model.Permission.objects

permission_query = PermissionQuery()
