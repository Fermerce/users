from faker import Faker
import httpx
import pytest
from src.app.permission import schema
from src.app.permission import service


@pytest.mark.asyncio
async def test_create_customer(faker: Faker, client: httpx.AsyncClient):
    res = await client.get("/api/v1/permissions/example/testing")
    print(res.json(), res.status_code)
