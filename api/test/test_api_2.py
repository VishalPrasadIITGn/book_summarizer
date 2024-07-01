import pytest
from fastapi.testclient import TestClient
from book_summarizer.api.main import app
from book_summarizer.db.schema.schemas import BookCreate, BookUpdate, ReviewCreate
from book_summarizer.db.session import DBSession
import json
import asyncio
from book_summarizer.db.cruds.crud_books import crud_book
from book_summarizer.db.cruds.crud_reviews import crud_review
from absl.testing import absltest
client = TestClient(app)


class TestAPI(absltest.TestCase):
  """API test class."""
  def setUp(self):
    """Setup."""
    _ = asyncio.run(self.delete_everything())

  def tearDown(self):
    """TearDown."""
    _ = asyncio.run(self.delete_everything())

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

  def test_create_book(self) -> None:
    """Test case for create book"""
    _ = asyncio.run(self.delete_everything())
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "genre": "Test Genre",
        "year_published": 2021,
        "summary": "Test Summary",
        "id":1
    }
    response = client.post("/books", json=book_data)
    assert response.status_code == 200
    assert response.json()[0]["title"] == book_data["title"]
    
  def test_get_books(self) -> None:
    """Test case for get book"""
    _ = asyncio.run(self.delete_everything())
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "genre": "Test Genre",
        "year_published": 2021,
        "summary": "Test Summary",
        "id":1
    }
    response = client.post("/books", json=book_data)
    assert response.status_code == 200
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json())>0
    db_dict = response.json()[0]
    assert sorted(list(db_dict.keys()))==sorted(["title", "author", "genre", "year_published", "summary", "id"])

  def test_get_book_two(self) -> None:
      """Test case for get book"""
      _ = asyncio.run(self.delete_everything())
      book_data = {
          "title": "Test Book 2",
          "author": "Test Author 2",
          "genre": "Test Genre 2",
          "year_published": 2022,
          "summary": "Test Summary 2",
          "id": 2
      }
      create_response = client.post("/books", json=book_data)
      assert create_response.status_code==200
      book_id = create_response.json()[0]["id"]
      response = client.get(f"/books/{book_id}")
      assert response.status_code == 200
      assert response.json()["title"] == book_data["title"]

  def test_update_book(self) -> None:
    """Test case for update book"""
    _ = asyncio.run(self.delete_everything())
    book_data = {
        "title": "Test Book 3",
        "author": "Test Author 3",
        "genre": "Test Genre 3",
        "year_published": 2023,
        "summary": "Test Summary 3",
        "id": 3
    }
    create_response = client.post("/books", json=book_data)
    assert create_response.status_code==200
    book_id = create_response.json()[0]["id"]
    update_data = {
        "id": book_id,
        "title": "Updated Test Book",
        "author": "Updated Test Author",
        "genre": "Updated Test Genre",
        "year_published": 2024,
        "summary": "Updated Test Summary"
    }
    response = client.put(f"/books/{book_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == update_data["title"]
    
  def test_delete_book(self) -> None:
    """Test case for delete book"""

    _ = asyncio.run(self.delete_everything())
    book_data = {
        "title": "Test Book 4",
        "author": "Test Author 4",
        "genre": "Test Genre 4",
        "year_published": 2024,
        "summary": "Test Summary 4",
        "id":1
    }
    create_response = client.post("/books", json=book_data)
    assert create_response.status_code==200
    book_id = book_data["id"]
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["title"] == book_data["title"]
    
  def test_create_review(self) -> None:
    _ = asyncio.run(self.delete_everything())
    book_data = {
        "title": "Test Book 5",
        "author": "Test Author 5",
        "genre": "Test Genre 5",
        "year_published": 2025,
        "summary": "Test Summary 5",
        "id":5
    }
    create_response = client.post("/books", json=book_data)
    assert create_response.status_code==200
    book_id = create_response.json()[0]["id"]
    review_data = {
        "book_id": book_id,
        "review_text": "Great book!",
        "rating": 5,
        "user_id": "something",
        "id": 1
    }
    
    response = client.post(f"/books/{book_id}/reviews", json=review_data)
    assert response.status_code == 200
    assert response.json()["review_text"] == review_data["review_text"]
    
  def test_get_reviews(self) -> None:
    _ = asyncio.run(self.delete_everything())
    book_data = {
        "title": "Test Book 6",
        "author": "Test Author 6",
        "genre": "Test Genre 6",
        "year_published": 2026,
        "summary": "Test Summary 6",
        "id":1
    }
    create_response = client.post("/books", json=book_data)
    assert create_response.status_code==200
    book_id = create_response.json()[0]["id"]
    review_data = {
        "book_id": book_id,
        "review_text": "Another great book!",
        "rating": 4,
        "user_id": "something",
        "id": 4
    }
    client.post(f"/books/{book_id}/reviews", json=review_data)
    response = client.get(f"/books/{book_id}/reviews")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
  def test_get_book_summary(self) -> None:
    """Test get summary for book"""
    
    _ = asyncio.run(self.delete_everything())
    book_id = 1
    book_data = {
        "title": "Test Book 7",
        "author": "Test Author 7",
        "genre": "Test Genre 7",
        "year_published": 2027,
        "summary": "Test Summary 7",
        "id":book_id
    }
    create_response = client.post("/books", json=book_data)
    assert create_response.status_code==200
    
    review_data = {
        "book_id": book_id,
        "review_text": "Another great book!",
        "rating": 4,
        "user_id": "something",
        "id": 4
    }
    client.post(f"/books/{book_id}/reviews", json=review_data)
    response = client.get(f"/books/{book_id}/reviews")

    review_data = {
        "book_id": book_id,
        "review_text": "Another great book!",
        "rating": 4,
        "user_id": "something",
        "id": 5
    }
    client.post(f"/books/{book_id}/reviews", json=review_data)
    
    review_data = {
        "book_id": book_id,
        "review_text": "Another great book!",
        "rating": 1,
        "user_id": "something",
        "id": 6
    }
    client.post(f"/books/{book_id}/reviews", json=review_data)
    response = client.get(f"/books/{book_id}/reviews")
    response = client.get(f"/books/{book_id}/reviews")
    book_id = create_response.json()[0]["id"]
    response = client.get(f"/books/{book_id}/summary")
    assert response.status_code == 200
    assert "summary" in response.json()
    assert response.json()["average_rating"] == 3
    assert response.json()["review_count"] == 3

  def test_generate_summary(self) -> None:
    """Test generate summary for content"""
    
    _ = asyncio.run(self.delete_everything())
    content = "This is the content of the book to be summarized."
    response = client.post("/generate-summary", params={"content": content})
    print(response.json())
    assert response.status_code == 200
    assert "summary" in response.json()




