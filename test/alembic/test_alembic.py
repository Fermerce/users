from sqlalchemy import text
import pytest
from lib.db.config import engine


@pytest.mark.asyncio
async def test_alembic_migration():
    async with engine.connect() as conn:
        stmt = text("SELECT COUNT(*) FROM alembic_version")
        result = await conn.execute(stmt)
        result = result.scalar()
        assert result != 0
