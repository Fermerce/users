import typing as t
import pytest
import pytest_asyncio
import httpx
from src.lib.db.config import async_session
from sqlalchemy.ext.asyncio import AsyncSession
from alembic.config import Config
from alembic import command
import main
from src.lib.base import settings
from db.config import engine


@pytest.fixture(autouse=True)
def db_engine():
    settings.config.environment = "testing"
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", str(engine.url))
    try:
        command.downgrade(alembic_cfg, "head")
    except Exception:
        pass
    command.upgrade(alembic_cfg, "head")
    yield
    command.downgrade(alembic_cfg, "head")


@pytest_asyncio.fixture
async def get_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest_asyncio.fixture
async def client() -> t.AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(app=main.app, base_url="http://testserver") as client:
        client.base_url = str(client.base_url).rstrip("/") + "/"
        yield client
