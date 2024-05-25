from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .string_connection import db_string


engine = create_async_engine(db_string.ASYNC_CONNECTION, echo=False)
SessionLocal = async_sessionmaker(engine)
