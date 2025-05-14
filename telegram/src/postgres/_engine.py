from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import settings

engine = create_async_engine(
    f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
)
async_session = async_sessionmaker(engine, expire_on_commit=False)
