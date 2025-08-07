# app/db/session.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from ..config.settings import settings

DATABASE_URL = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")

# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=settings.debug, future=True)

# Create session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# Declarative base
Base = declarative_base()

# Dependency for FastAPI routes
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
