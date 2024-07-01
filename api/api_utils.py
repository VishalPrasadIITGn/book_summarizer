"""Utils for APIs and router"""
from typing import Generator
from book_summarizer.db.session import DBSession

def get_db() -> Generator:
  """Returns the db session."""
  db = DBSession()
  try:
    yield db
  finally:
    db.close()
