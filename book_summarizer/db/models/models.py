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
# from sqlalchemy.orm import mapped_column

from book_summarizer.db.models.base_class import Base
metadata = Base.metadata

# class Books(Base):
#   """Dataset class for entry to dataset table."""

#   __tablename__ = "books"

#   id: Mapped[int] = Column(Integer, index=True, unique=True, primary_key=True)
#   title = Column(String, index=True)
#   author = Column(String, index=True)
#   genre = Column(String, index=True)
#   summary = Column(String, index=True)
#   year_published = Column(Integer, index=True)

#   # book_review = relationship("Reviews",
#   #                             back_populates="review_book",
#   #                             cascade='all, delete',
#   #                             foreign_keys="Reviews.id")
#   reviews: Mapped[list["Reviews"]] = relationship("Reviews", back_populates="books", foreign_keys="Reviews.id")


# class Reviews(Base):
#   """Lease class for lease documents."""
#   __tablename__ = "reviews"

#   # id = Column(Integer, index=True, unique=True, primary_key=True)

#   id: Mapped[int] = Column(index=True, primary_key=True, unique=True)
#   # book_id: Mapped[int] = Column(ForeignKey("Books.id"))
#   book_id: Mapped[int] = Column(ForeignKey("books.id"), index=True)
#   books: Mapped["Books"] = relationship("Books", back_populates="reviews", foreign_keys="Books.id")

#   # book_id = Column(Integer, ForeignKey("books.id"))
#   user_id = Column(String, index=True)
#   review_text = Column(String, index=True)
#   rating = Column(Integer, index=True)

#   # review_book = relationship("Books",
#   #                           back_populates="book_review",
#   #                           cascade='all, delete',
#   #                           foreign_keys="Books.id")
  
"""SQLAlchemy ORM models for database."""

"""SQLAlchemy ORM models for database."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped
from book_summarizer.db.models.base_class import Base


# class Books(Base):
#     """Dataset class for entry to dataset table."""

#     __tablename__ = "books"

#     id: Mapped[int] = Column(Integer, index=True, unique=True, primary_key=True)
#     title = Column(String, index=True, unique=True)
#     author = Column(String, index=True)
#     genre = Column(String, index=True)
#     summary = Column(String, index=True)
#     year_published = Column(Integer, index=True)

#     reviews: Mapped[list["Reviews"]] = relationship("Reviews", back_populates="books", cascade='all, delete-orphan')


# class Reviews(Base):
#     """Lease class for lease documents."""

#     __tablename__ = "reviews"

#     id: Mapped[int] = Column(Integer, index=True, unique=True, primary_key=True)
#     book_id: Mapped[int] = Column(ForeignKey("books.id"), index=True)
#     user_id = Column(String, index=True)
#     review_text = Column(String, index=True)
#     rating = Column(Integer, index=True)

#     books: Mapped["Books"] = relationship("Books", back_populates="reviews", foreign_keys="books.id")


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