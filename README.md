# book_summarizer
books management system with summarizer using llama3

## Deploy using fastapi
git clone https://github.com/VishalPrasadIITGn/book_summarizer.git

run `cd book_summarizer`

run `poetry install`

run either of two commands:
1. `python book_summarizer/recommendation/prediction/make_prediction.py`
2. `gunicorn book_summarizer.api.main:app --bind 0.0.0.0:8000 --workers 4 --max-requests 2000 --max-requests-jitter 100 --worker-class uvicorn.workers.UvicornWorker --graceful-timeout 100 --reload`
access localhost:8000 to see the swagger

## Deploy using docker container
git clone 

https://github.com/VishalPrasadIITGn/book_summarizer.git

run `cd book_summarizer`

run the following command `docker run -p 8000:8000 book_rec:v1`

## Deploy using docker compose
git clone 
https://github.com/VishalPrasadIITGn/book_summarizer.git

run `cd book_summarizer`

Build the image `docker build --no-cache -t book_rec:v1 .`

run the command `docker-compose up`

