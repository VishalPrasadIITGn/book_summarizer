from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.future import select
import asyncio
from typing import List, Optional

# Database URL and session setup
DATABASE_URL = "postgresql+asyncpg://user:password123@10.113.34.11:8765/book_rec_2"
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    genre = Column(String, index=True)
    summary = Column(String, index=True)
    year_published = Column(Integer, index=True)
    reviews = relationship("Review", back_populates="book", cascade="all, delete")

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    user_id = Column(String, index=True)
    review_text = Column(String, index=True)
    rating = Column(Integer, index=True)
    book = relationship("Book", back_populates="reviews")

class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get_all(self, db: AsyncSession, skip: int = 0) -> Optional[List[Base]]:
        query = select(self.model).offset(skip)
        result = await db.execute(query)
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: dict) -> Base:
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

class CRUDBook(CRUDBase):
    pass

crud_book = CRUDBook(Book)

async def create_book_example():
    async with AsyncSessionLocal() as session:
        try:
            book_data = {
                "title": "Example Book Title",
                "author": "Example Author",
                "genre": "Fiction",
                "summary": "This is a summary of the example book.",
                "year_published": 2023,
            }
            new_book = await crud_book.create(db=session, obj_in=book_data)
            print(f"New book created: {new_book}")
        except Exception as e:
            print(f"An error occurred: {e}")
async def test_api():
    async with AsyncSessionLocal() as session:
        try:
            books = await crud_book.get_all(db=session)
            print([obj.__dict__ for obj in books])
        except Exception as e:
            print(f"An error occurred: {e}")
# Run the create book function
asyncio.run(create_book_example())
# Run the test function
asyncio.run(test_api())
