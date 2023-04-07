from functools import wraps
from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from core.settings import config
from sqlalchemy import MetaData
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
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
        connect_args={"check_same_thread": False},
    )
else:
    engine = create_async_engine(config.get_database_url(), echo=False)

Async_session: AsyncSession = async_sessionmaker(bind=engine, expire_on_commit=False)


@asynccontextmanager
async def async_session():
    session = Async_session()
    try:
        yield session
    except Exception as e:
        print(e, "here")
        await session.rollback()
    finally:
        await session.close()


def async_session(func):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            arg_to_list = list(args)
            if hasattr(args[0], "__class__"):
                self = arg_to_list[0]
                del arg_to_list[0]
                args = tuple(arg_to_list)
                return await func(self, session, *args, **kwargs)
            else:
                return await func(session, *args, **kwargs)

    return wrapper
