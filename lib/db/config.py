import time

from fastapi import FastAPI
import databases
import sqlalchemy

from core.settings import config


database = databases.Database(config.get_database_url())
metadata = sqlalchemy.MetaData(database)
engine = sqlalchemy.create_engine(config.get_database_url())


async def connect_database(app: FastAPI) -> None:
    app.state.database = database
    database_ = app.state.database
    while True:
        try:
            if not database_.is_connected:
                await database_.connect()
                if config.debug:
                    print("database connected")
                    break
        except Exception as _:
            time.sleep(5)


async def disconnect_database(app: FastAPI) -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()
        if config.debug:
            print("database disconnected")
