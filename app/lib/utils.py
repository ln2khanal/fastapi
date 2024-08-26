import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.lib.database import SessionLocal

async def get_db() -> AsyncSession: # type: ignore
    async with SessionLocal() as session:
        yield session