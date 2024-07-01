"""Test casesfor schemas"""

import pytest
from pydantic import ValidationError
# from book_summarizer.db import schemas
from book_summarizer.db.schema.schemas import BookCreate, Book, ReviewCreate, Review

def test_book_create_required_fields():
    """Test that BookCreate requires all fields"""
    with pytest.raises(ValidationError):
        BookCreate()

def test_book_create_with_all_fields():
    """Test that BookCreate works with all fields provided"""
    book = BookCreate(
        title="Sample Title",
        author="Sample Author",
        genre="Sample Genre",
        year_published=2021,
        summary="Sample Summary"
    )
    assert book.title == "Sample Title"
    assert book.author == "Sample Author"
    assert book.genre == "Sample Genre"
    assert book.year_published == 2021
    assert book.summary == "Sample Summary"

def test_book_create_missing_field():
    """Test that BookCreate raises error if a required field is missing"""
    with pytest.raises(ValidationError):
        BookCreate(
            title="Sample Title",
            author="Sample Author",
            genre="Sample Genre",
            year_published=2021
        )

def test_book_inherits_from_book_create():
    """Test that Book inherits from BookCreate and includes id"""
    book = Book(
        id=1,
        title="Sample Title",
        author="Sample Author",
        genre="Sample Genre",
        year_published=2021,
        summary="Sample Summary"
    )
    assert book.id == 1
    assert book.title == "Sample Title"
    assert book.author == "Sample Author"
    assert book.genre == "Sample Genre"
    assert book.year_published == 2021
    assert book.summary == "Sample Summary"

def test_review_create_required_fields():
    """Test that ReviewCreate requires all fields"""
    with pytest.raises(ValidationError):
        ReviewCreate()

def test_review_create_with_all_fields():
    """Test that ReviewCreate works with all fields provided"""
    review = ReviewCreate(
        book_id=1,
        user_id="Sample user",
        review_text="Sample review",
        rating=4,
    )
    assert review.book_id == 1
    assert review.user_id == "Sample user"
    assert review.review_text == "Sample review"
    assert review.rating == 4

def test_review_create_missing_field():
    """Test that ReviewCreate raises error if a required field is missing"""
    with pytest.raises(ValidationError):
        ReviewCreate(
            title="Sample Title",
            author="Sample Author",
            genre="Sample Genre",
            year_published=2021
        )

def test_review_inherits_from_review_create():
    """Test that Review inherits from ReviewCreate and includes id"""
    review = Review(
        id=1,
        book_id=1,
        user_id="Sample user",
        review_text="Sample review",
        rating=4,
    )
    assert review.id == 1
    assert review.book_id == 1
    assert review.user_id == "Sample user"
    assert review.review_text == "Sample review"
    assert review.rating == 4

# Negative test cases

def test_book_create_invalid_year_published():
    """Test that BookCreate raises error if year_published is not an integer"""
    with pytest.raises(ValidationError):
        BookCreate(
            title="Sample Title",
            author="Sample Author",
            genre="Sample Genre",
            year_published="invalid_year",
            summary="Sample Summary"
        )

def test_book_create_invalid_genre():
    """Test that BookCreate raises error if genre is not a string"""
    with pytest.raises(ValidationError):
        BookCreate(
            title="Sample Title",
            author="Sample Author",
            genre=123,
            year_published=2021,
            summary="Sample Summary"
        )

def test_review_create_invalid_rating():
    """Test that ReviewCreate raises error if rating is out of range"""
    with pytest.raises(ValidationError):
        ReviewCreate(
            title="Sample Title",
            author="Sample Author",
            genre="Sample Genre",
            year_published=2021,
            summary="Sample Summary",
            rating=6  # Invalid rating, should be between 1 and 5
        )

def test_review_create_invalid_review_text():
    """Test that ReviewCreate raises error if review_text is not a string"""
    with pytest.raises(ValidationError):
        ReviewCreate(
            title="Sample Title",
            author="Sample Author",
            genre="Sample Genre",
            year_published=2021,
            summary="Sample Summary",
            review_text=12345  # Invalid review_text, should be a string
        )

