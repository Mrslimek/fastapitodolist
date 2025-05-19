from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings


engine = create_async_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession)


async def get_db():
    async with SessionLocal() as session:
        yield session


class Base(DeclarativeBase):
    pass
