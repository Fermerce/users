import httpx
import pytest
from core.src.base.settings import config


@pytest.mark.asyncio
async def test_health_check(client: httpx.AsyncClient):
    res = await client.get("/")
    data = res.json()
    data["name"] = config.project_name
    data["version"] = config.project_version
    data["description"] = config.project_description
    assert res.status_code == 200
