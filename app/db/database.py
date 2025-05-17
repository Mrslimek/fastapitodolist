from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings


# TODO: Убрать потом echo=True
engine = create_async_engine(settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession)


async def get_db():
    async with SessionLocal() as session:
        yield session


class Base(DeclarativeBase):
    pass
