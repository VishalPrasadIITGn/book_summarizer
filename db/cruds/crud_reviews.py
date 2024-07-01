"""CRUD for reviews table"""

from book_summarizer.db.cruds.crud_base import CRUDBase
from book_summarizer.db.models.models import Reviews
from book_summarizer.db.schema.schemas import ReviewCreate
from book_summarizer.db.schema.schemas import ReviewUpdate


class CRUDReview(CRUDBase[Reviews, ReviewCreate, ReviewUpdate]):
  """CRUD operation for document table."""

crud_review = CRUDReview(Reviews, "id")
