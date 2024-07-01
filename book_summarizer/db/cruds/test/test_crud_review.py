# mypy: ignore-errors
"""Test cases for review CRUD operations."""

import asyncio
import pytest

from book_summarizer.db.cruds.crud_reviews import crud_review
from book_summarizer.db.schema.schemas import ReviewCreate
from book_summarizer.db.session import DBSession
from book_summarizer.db.cruds.crud_books import crud_book
from book_summarizer.db.schema.schemas import Review, ReviewCreate, BookCreate, ReviewUpdate, BookUpdate

@pytest.mark.asyncio
class TestReview:
    """Test CRUD operations for the reviews table."""

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

    async def test_create_review(self):
      """Test creation of a review."""
      async with DBSession() as session:
        # Create books for the review to reference
        await self.delete_everything()
        db_input_book_a = await crud_book.create_with_name(
            db=session,
            obj_inputs=[BookCreate(**{
                "title": "book_1_test",
                "author": "Author 1",
                "genre": "Genre 1",
                "year_published": 2021,
                "summary": "Summary 1",
                "id":1
            })]
        )
        db_input_book_b = await crud_book.create_with_name(
            db=session,
            obj_inputs=[BookCreate(**{
                "title": "book_2_test",
                "author": "Author 2",
                "genre": "Genre 2",
                "year_published": 2022,
                "summary": "Summary 2",
                "id": 2
            })]
        )

        # Define review creation inputs
        db_input_review_a = ReviewCreate(
            review_text="Review 1",
            rating=4,
            book_id=db_input_book_a[0].id,
            user_id="user"
        )
        db_input_review_b = ReviewCreate(
            review_text="Review 2",
            rating=3,
            book_id=db_input_book_b[0].id,
            user_id="user"
        )

        # Create reviews
        db_output_a = await crud_review.create(db=session, obj_inputs=[db_input_review_a])
        db_output_b = await crud_review.create(db=session, obj_inputs=[db_input_review_b])

        # Assert creation results
        db_output_a = db_output_a[0]
        db_output_b = db_output_b[0]
        assert db_output_a
        assert db_output_a.review_text == db_input_review_a.review_text
        assert db_output_a.rating == db_input_review_a.rating
        assert db_output_a.book_id == db_input_review_a.book_id

        assert db_output_b
        assert db_output_b.review_text == db_input_review_b.review_text
        assert db_output_b.rating == db_input_review_b.rating
        assert db_output_b.book_id == db_input_review_b.book_id

    async def test_update_review(self):
      """Test updating a review."""
      async with DBSession() as session:
        # Delete existing reviews and books before test
        await self.delete_everything()
        # Create a book for the review to reference
        db_input_book = await crud_book.create_with_name(
            db=session,
            obj_inputs=[BookCreate(**{
                "title": "book_1_test",
                "author": "Author 1",
                "genre": "Genre 1",
                "year_published": 2021,
                "summary": "Summary 1",
                "id": 1
            })]
        )

        # Create a review to update
        db_input_review = Review(
            review_text="Initial Review",
            rating=4,
            book_id=db_input_book[0].id,
            user_id="1",
            id=2
        )

        async with DBSession() as session:

            # Create the initial review
            db_output = await crud_review.create(db=session, obj_inputs=[db_input_review])
            db_output=db_output[0]
            # Assert creation result
            assert db_output
            assert db_output.review_text == db_input_review.review_text
            assert db_output.rating == db_input_review.rating
            assert db_output.book_id == db_input_review.book_id

            # Update the review
            # updated_review = db_output.copy(update=ReviewUpdate(**{
            #     "content": "Updated Review",
            #     "rating": 4
            # }))
            db_input_review.rating = 1
            db_input_review.review_text = "Updated Review"

            db_updated_output = await crud_review.update(db=session, obj_in=db_input_review)

            # Assert update result
            assert db_updated_output
            assert db_updated_output.review_text == "Updated Review"
            assert db_updated_output.rating == 1
            assert db_updated_output.book_id == db_input_review.book_id

    async def test_delete_review(self):
        """Test deleting a review."""
        async with DBSession() as session:
          # Delete existing reviews and books before test
          await self.delete_everything()
          # Create a book for the review to reference
          db_input_book = await crud_book.create_with_name(
              db=session,
              obj_inputs=[BookCreate(**{
                  "title": "book_1_test",
                  "author": "Author 1",
                  "genre": "Genre 1",
                  "year_published": 2021,
                  "summary": "Summary 1",
                  "id":1
              })]
          )

          # Create a review to delete
          db_input_review = Review(
            review_text="Initial Review",
            rating=4,
            book_id=db_input_book[0].id,
            user_id="1",
            id=2
        )

          # Create the review to delete
          db_output = await crud_review.create(db=session, obj_inputs=[db_input_review])
          db_output = db_output[0]
          # Assert creation result
          assert db_output
          assert db_output.review_text == db_input_review.review_text
          assert db_output.rating == db_input_review.rating
          assert db_output.book_id == db_input_review.book_id

          # Delete the review
          await crud_review.delete(db=session, id_value=db_output.id)

          # Attempt to retrieve the deleted review
          deleted_review = await crud_review.get(db=session, search_value=db_output.id)

          # Assert deletion result
          assert deleted_review is None
