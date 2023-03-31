import sqlalchemy as sa
from src.app.customer.model import Customer


async def test_create_model():
    register_columns = [
        ("firstname", "VARCHAR(20)"),
        ("lastname", "VARCHAR(20)"),
        ("username", "VARCHAR(30)"),
        ("email", "VARCHAR(50)"),
        ("password", "VARCHAR"),
        ("password_reset_token", "VARCHAR"),
        ("is_verified", "BOOLEAN"),
        ("is_suspended", "BOOLEAN"),
        ("is_active", "BOOLEAN"),
        ("id", "CHAR(32)"),
        ("created_at", "DATETIME"),
        ("updated_at", "DATETIME"),
    ]
    register_relationships = [("permissions", "permission")]
    current_relationships = [
        (rel.key, rel.target.name) for rel in sa.inspect(Customer).relationships
    ]
    current_columns = [
        (column.name, str(column.type)) for column in sa.inspect(Customer).c
    ]
    assert Customer.__tablename__ == "customer"

    for rel1, rel2 in zip(current_relationships, register_relationships):
        assert rel1[0] == rel2[0]
        assert rel1[1] == rel2[1]

    for t1, t2 in zip(current_columns, register_columns):
        assert t1[0] == t2[0]
        assert t1[1] == t2[1]
