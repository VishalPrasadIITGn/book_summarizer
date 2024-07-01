# mypy: ignore-errors
"""Test cases for book CRUD operations."""

import asyncio
import pytest

from book_summarizer.db.cruds.crud_books import crud_book
from book_summarizer.db.schema.schemas import BookCreate
from book_summarizer.db.session import DBSession
from book_summarizer.db.cruds.crud_books import crud_book
from book_summarizer.db.cruds.crud_reviews import crud_review


@pytest.mark.asyncio
class TestBook:
    """Test CRUD operations for the books table."""
    async def delete_everything(self) -> None:
        async with DBSession() as session:
            # Delete all existing reviews
            existing_reviews = await crud_review.get_all(db=session)
            review_ids = [review.id for review in existing_reviews]
            await crud_review.delete_multiple(db=session, obj_inputs=review_ids)

            # Delete all existing books
            existing_books = await crud_book.get_all(db=session)
            book_ids = [book.id for book in existing_books]
            await crud_book.delete_multiple(db=session, obj_inputs=book_ids)
    async def test_create_book(self):
        """Test creation of a book."""
        
        db_input_a = BookCreate(
            title="book_1_test",
            author="Author 1",
            genre="Genre 1",
            year_published=2021,
            summary="Summary 1",
            id=1
        )
        db_input_b = BookCreate(
            title="book_2_test",
            author="Author 2",
            genre="Genre 2",
            year_published=2022,
            summary="Summary 2",
            id=2
        )

        async with DBSession() as session:
            # Delete all existing reviews
            existing_reviews = await crud_review.get_all(db=session)
            review_ids = [review.id for review in existing_reviews]
            await crud_review.delete_multiple(db=session, obj_inputs=review_ids)

            # Delete all existing books
            existing_books = await crud_book.get_all(db=session)
            book_ids = [book.id for book in existing_books]
            await crud_book.delete_multiple(db=session, obj_inputs=book_ids)

            db_output_a = await crud_book.create_with_name(db=session, obj_inputs=[db_input_a])
            db_output_b = await crud_book.create_with_name(db=session, obj_inputs=[db_input_b])
            db_output_b = db_output_b[0]
            assert db_output_a
            assert db_output_a[0].title == db_input_a.title
            assert db_output_a[0].author == db_input_a.author
            assert db_output_a[0].genre == db_input_a.genre
            assert db_output_a[0].year_published == db_input_a.year_published
            assert db_output_a[0].summary == db_input_a.summary

            assert db_output_b
            assert db_output_b.title == db_input_b.title
            assert db_output_b.author == db_input_b.author
            assert db_output_b.genre == db_input_b.genre
            assert db_output_b.year_published == db_input_b.year_published
            assert db_output_b.summary == db_input_b.summary


    async def test_update_book(self):
        """Test updating a book."""
        db_input_a = BookCreate(
            title="book_1_test",
            author="Author 1",
            genre="Genre 1",
            year_published=2021,
            summary="Summary 1",
            id=1
        )
        db_input_b = BookCreate(
            title="book_2_test",
            author="Author 2",
            genre="Genre 2",
            year_published=2022,
            summary="Summary 2",
            id=2
        )

        async with DBSession() as session:
            # Delete all existing reviews
            existing_reviews = await crud_review.get_all(db=session)
            review_ids = [review.id for review in existing_reviews]
            await crud_review.delete_multiple(db=session, obj_inputs=review_ids)

            # Delete all existing books
            existing_books = await crud_book.get_all(db=session)
            book_ids = [book.id for book in existing_books]
            await crud_book.delete_multiple(db=session, obj_inputs=book_ids)

            db_output_a = await crud_book.create_with_name(db=session, obj_inputs=[db_input_a])
            db_output_b = await crud_book.create_with_name(db=session, obj_inputs=[db_input_b])

            assert db_output_a
            # db_output_a = db_output_a[0]
            assert db_output_a[0].title == db_input_a.title

            db_input_a.title = "updated_title"
            db_input_b.genre = "new_genre"
            updated_db_input_book_list = [db_input_a, db_input_b]
            updated_books = await crud_book.update_multiple(db=session, obj_inputs=updated_db_input_book_list)

            assert updated_books[0].title == "updated_title"
            assert updated_books[1].genre == "new_genre"

    async def test_delete_book(self):
        """Test deleting a book."""
        db_input_a = BookCreate(
            title="book_1_test",
            author="Author 1",
            genre="Genre 1",
            year_published=2021,
            summary="Summary 1",
            id=1
        )
        db_input_b = BookCreate(
            title="book_2_test",
            author="Author 2",
            genre="Genre 2",
            year_published=2022,
            summary="Summary 2",
            id=2
        )

        async with DBSession() as session:
            # Delete all existing reviews
            existing_reviews = await crud_review.get_all(db=session)
            review_ids = [review.id for review in existing_reviews]
            await crud_review.delete_multiple(db=session, obj_inputs=review_ids)

            # Delete all existing books
            existing_books = await crud_book.get_all(db=session)
            book_ids = [book.id for book in existing_books]
            await crud_book.delete_multiple(db=session, obj_inputs=book_ids)
            db_output_a = await crud_book.create_with_name(db=session, obj_inputs=[db_input_a])
            db_output_b = await crud_book.create_with_name(db=session, obj_inputs=[db_input_b])

            assert db_output_a
            assert db_output_a[0].title == db_input_a.title

            await crud_book.delete_multiple(db=session, obj_inputs=[db_output_a[0].id, db_output_b[0].id])
            deleted_book_a = await crud_book.get(db=session, search_value=db_output_a[0].id)
            deleted_book_b = await crud_book.get(db=session, search_value=db_output_b[0].id)

            assert deleted_book_a is None
            assert deleted_book_b is None
