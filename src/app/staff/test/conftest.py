import pytest_asyncio
import pytest


@pytest_asyncio.fixture(scope="session")
async def new_Customer():
    pass
