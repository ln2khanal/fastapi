import pytest
from app.main import app
from httpx import AsyncClient, ASGITransport
from app.lib.database import engine, async_session, Base


@pytest.fixture(scope="module")
async def db_session():
    async with async_session() as session:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield session
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="module")
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost/api/v1"
    ) as client:
        yield client
