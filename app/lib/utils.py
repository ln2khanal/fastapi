import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.lib.database import async_session


async def get_db() -> AsyncSession:  # type: ignore
    async with async_session() as session:
        yield session
