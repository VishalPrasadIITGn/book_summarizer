FROM python:3.11-slim-buster

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev libpq-dev libmagic1 && \
    pip install --upgrade pip --no-cache-dir && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set up the app directory
WORKDIR /app

# Copy the application code
COPY . /app

# Set PYTHONPATH environment variable
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Install Poetry
RUN pip install poetry --no-cache-dir

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi && rm -rf /root/.cache/

# Command to run the application
CMD ["gunicorn", "book_summarizer.api.main:app", "--bind", "0.0.0.0:8000", "--workers", "4", "--reload", "--max-requests", "2000", "--max-requests-jitter", "100", "--worker-class", "uvicorn.workers.UvicornWorker", "--graceful-timeout", "180", "--timeout", "0"]
# CMD ["uvicorn" , "ca.api.main:app" , "--port" ,"8022", "--host" ,"0.0.0.0", "--reload"]
