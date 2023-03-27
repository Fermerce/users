# import all apps model to this file for alembic migration access
from src.app.customer.model import Customer
from src.app.staff.model import Staff
from src.app.permission.model import Permission
from src.app.auth.model import AuthToken

model_for_alembic = [Customer, Staff, Permission, AuthToken]
