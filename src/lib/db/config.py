from src._base.settings import config
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
)

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

metadata = MetaData()
Model = declarative_base(metadata=metadata)

engine = None
if str(config.get_database_url()).startswith("sqlite+aiosqlite"):
    engine = create_async_engine(
        config.get_database_url(),
        echo=False,
        future=True,
        connect_args={"check_same_thread": False},
    )
else:
    engine = create_async_engine(config.get_database_url(), echo=False, future=True)

async_session: AsyncSession = sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)
