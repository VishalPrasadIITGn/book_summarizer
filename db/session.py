"""Database session creation module."""

from typing import Tuple

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from book_summarizer.config.config import setting
from sqlalchemy.pool import NullPool

# def create_session() -> Tuple:
#   """Database session creation."""
#   engine = create_engine(setting.SQLALCHEMY_DATABASE_URL) # pylint: disable=redefined-outer-name
#   db_session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
#   return engine, db_session


# engine, DBSession = create_session()



from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


# engine = create_async_engine(setting.SQLALCHEMY_DATABASE_URL, echo=True)
# async_session = sessionmaker(
#     engine, expire_on_commit=False, class_=AsyncSession
# )

def create_session() -> Tuple:
  """Database session creation."""
  engine = create_async_engine(setting.SQLALCHEMY_DATABASE_URL, echo=True, poolclass=NullPool)
  async_session = sessionmaker(
      engine, expire_on_commit=False, class_=AsyncSession
  )
  return engine, async_session


engine, DBSession = create_session()