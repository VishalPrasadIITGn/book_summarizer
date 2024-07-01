"""Schema for databases"""

from datetime import datetime
from typing import Any, Literal

from passlib.context import CryptContext
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AllOptional(BaseModel):
  """Make all fields optional."""

  @classmethod
  def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
    super().__pydantic_init_subclass__(**kwargs)

    for field in cls.model_fields.values():
      if field.is_required():
        field.default = None

    cls.model_rebuild(force=True)

class BookCreate(BaseModel):
  """Schema for book creation"""
  id: int = Field(description="Title of the book")
  title: str = Field(description="Title of the book")
  author: str = Field(description="Author of the book")
  genre: str = Field(description="Genre of the book")
  year_published: int = Field(description="Year of the book")
  summary: str = Field(description="Summary of the book")
    


class Book(BookCreate):
  """Schema for book"""
  id: int
  
class BookUpdate(AllOptional, BookCreate): # pylint: disable=invalid-metaclass
  """BookUpdate class for update operations."""


class ReviewCreate(BaseModel):
  """Schema for review creation"""
  book_id: int = Field(description="ID of the book")
  user_id: str = Field(description="Author of the book")
  review_text: str = Field(description="Genre of the book")
  rating: Literal[1,2,3,4,5] = Field(description="Rating of the book")

class Review(ReviewCreate):
  """Schema for review"""
  id: int
  
class ReviewUpdate(AllOptional, ReviewCreate): # pylint: disable=invalid-metaclass
  """ReviewUpdate class for update operations."""


