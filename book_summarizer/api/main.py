from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Any
import logging

from book_summarizer.api.api_utils import get_db
from book_summarizer.db.cruds.crud_books import crud_book
from book_summarizer.db.cruds.crud_reviews import crud_review
from book_summarizer.db.schema import schemas
from book_summarizer.utils.exception_utils import AlreadyExistsError
from book_summarizer.llm.llm_summarize import get_content_summary
from book_summarizer.config.config import setting
from book_summarizer.db.session import DBSession
from book_summarizer.recommendation.prediction.make_prediction import predict

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

app = FastAPI()

# Endpoint to add a new book
@app.post("/books", response_model=list[schemas.Book])
async def create_book(book: schemas.Book):
    try:
      async with DBSession() as session:
        return await crud_book.create_with_name(db=session, obj_inputs=[book])
    except AlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong")

# Endpoint to retrieve all books
@app.get("/books", response_model=List[schemas.Book])
async def get_books():
    try:
      async with DBSession() as session:
        return await crud_book.get_all(db=session)
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong")

# Endpoint to retrieve a specific book by its ID
@app.get("/books/{id}", response_model=schemas.Book)
async def get_book(id: int):
    try:
      async with DBSession() as session:
        book = await crud_book.search_by_multiple_column(db=session, search_dict={"id":id})
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return book[0]
    except HTTPException as e:
        logger.error(f"Book with id `{id}` not found")
        raise HTTPException(status_code=404, detail=f"Book with `{id}` not found")
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong")

# Endpoint to update a book's information by its ID
@app.put("/books/{id}", response_model=schemas.Book)
async def update_book(book: schemas.BookUpdate):
    try:
      async with DBSession() as session:
        updated_book = await crud_book.update(db=session, obj_in=book)
        if not updated_book:
            raise HTTPException(status_code=404, detail="Book not found")
        return updated_book

    except HTTPException as e:
      logger.error(f"Book with id `{book.id}` not found")
      raise HTTPException(status_code=404, detail=f"Book with `{book.id}` not found")
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Something went wrong")

# Endpoint to delete a book by its ID
@app.delete("/books/{id}", response_model=schemas.Book)
async def delete_book(id: int, db: Session = Depends(get_db)):
    try:
        deleted_book = await crud_book.delete(db=db, id_value=id)
        if not deleted_book:
            raise HTTPException(status_code=404, detail="Book not found")
        return deleted_book
    except HTTPException as e:
      logger.error(f"Book with id `{id}` not found")
      raise HTTPException(status_code=404, detail=f"Book with `{id}` not found")
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong")

# Endpoint to add a review for a book
@app.post("/books/{id}/reviews", response_model=schemas.Review)
async def create_review(review: schemas.Review, db: Session = Depends(get_db)):
    try:
        # review.book_id = book_id
        review = await crud_review.create_with_name(db=db, obj_inputs=[review])
        return review[0]
    except (AlreadyExistsError, HTTPException, SQLAlchemyError) as e:
        logger.error(f"Database error occurred: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong")

# Endpoint to retrieve all reviews for a book
@app.get("/books/{id}/reviews", response_model=List[schemas.Review])
async def get_reviews(id: int):
    try:
      async with DBSession() as session:
        reviews = await crud_review.search_by_multiple_column(db=session, search_dict={"book_id":id})
        if not reviews:
            raise HTTPException(status_code=404, detail="No reviews found for this book")
        return reviews
    except HTTPException as e:
        logger.error(f"Database error occurred: {str(e)}")
        raise HTTPException(status_code=400, detail="No reviews found for this book")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong")

# Endpoint to get a summary and aggregated rating for a book
@app.get("/books/{id}/summary", response_model=dict[str, Any])
async def get_book_summary(id: int, db: Session = Depends(get_db)):
    try:
      book = await crud_book.get(db=db, search_value=id)
      if not book:
          raise HTTPException(status_code=404, detail="Book not found")

      reviews = await crud_review.search_by_multiple_column(db=db, search_dict={"book_id":id})
      if not reviews:
          return {"summary": book.summary, "average_rating": None, "review_count": 0}

      total_rating = sum([review.rating for review in reviews])
      average_rating = total_rating / len(reviews)

      return {"summary": book.summary, "average_rating": average_rating, "review_count": len(reviews)}

    except HTTPException as e:
        logger.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Book id `{id}` not found")
    except SQLAlchemyError as e:
        logger.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"A database occurred: {str(e)}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong")

# Endpoint to generate a summary for a given book content
@app.post("/generate-summary")
async def generate_summary(content: str):
    try:
        summary = get_content_summary(content=content, model_name=setting.LLM_MODEL_NAME, prompt_name=setting.LLM_PROMPT)
        return {"summary": summary}
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong")

# Endpoint to retrieve all reviews for a book
@app.get("/recommendations/{user_id}", response_model=list)
async def get_reviews(user_id: int):
    try:
        recommendations = predict(user_id)
        return recommendations
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
