"""CRUD for books table"""

from book_summarizer.db.cruds.crud_base import CRUDBase
from book_summarizer.db.models.models import Books
from book_summarizer.db.schema.schemas import BookCreate
from book_summarizer.db.schema.schemas import BookUpdate


class CRUDBook(CRUDBase[Books, BookCreate, BookUpdate]):
  """CRUD operation for document table."""

crud_book = CRUDBook(Books, "id")
