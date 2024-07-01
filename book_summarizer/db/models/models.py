"""SQLAlchemy ORM models for database."""

from sqlalchemy import ARRAY
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import String
# from sqlalchemy import List
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from sqlalchemy.orm import Mapped

from book_summarizer.db.models.base_class import Base
metadata = Base.metadata


# from sqlalchemy import Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship, Mapped
# from book_summarizer.db.models.base_class import Base


class Books(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    genre = Column(String, index=True)
    summary = Column(String, index=True)
    year_published = Column(Integer, index=True)
    reviews = relationship("Reviews", back_populates="book", cascade="all, delete")

class Reviews(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    user_id = Column(String, index=True)
    review_text = Column(String, index=True)
    rating = Column(Integer, index=True)
    book = relationship("Books", back_populates="reviews")