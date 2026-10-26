import os
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

raw_db_url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

# Fix Render's postgres:// prefix for SQLAlchemy compatibility
if raw_db_url.startswith("postgres://"):
    raw_db_url = raw_db_url.replace("postgres://", "postgresql+asyncpg://", 1)
elif raw_db_url.startswith("postgresql://"):
    raw_db_url = raw_db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(raw_db_url, echo=False, future=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session