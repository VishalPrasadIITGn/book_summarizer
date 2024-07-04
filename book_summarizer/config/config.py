"""Setting different variables related to api and redis connection."""
import os
from typing import Any
from pydantic import field_validator
from pydantic import PostgresDsn
from pydantic import ValidationInfo
from pydantic_settings import BaseSettings
from book_summarizer.llm.prompts.book_prompt import book_summary_prompt

class Settings(BaseSettings):
  """Environment variables."""


  # LLM_MODEL_NAME: str="meta-llama/Meta-Llama-3-8B-Instruct"
  LLM_MODEL_NAME: str = "microsoft/Phi-3-mini-128k-instruct"
  LLM_PROMPT: str = book_summary_prompt

  LRU_CACHE_SIZE: int = 3

  DB_USERNAME: str = os.getenv("DB_USERNAME") or "user"
  DB_PASSWORD: str = os.getenv("DB_PASSWORD") or "password123"
  DB_NAME: str = "book_rec_2"

  DB_HOST: str = "0.0.0.0"
  DB_PORT: int = 8765
  DB_SCHEME: str = "postgresql"
  SQLALCHEMY_DATABASE_URL: PostgresDsn | None = "postgresql://user:password123@0.0.0.0:8765/book_rec_2"

  @field_validator("SQLALCHEMY_DATABASE_URL", mode="after")
  @classmethod
  def db_connection(cls, v: str | None, info: ValidationInfo) -> Any:
    # pylint: disable=no-self-argument
    if isinstance(v, str):
      return v
    return str(
        PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=info.data["DB_USERNAME"],
            password=info.data["DB_PASSWORD"],
            host=f"{info.data['DB_HOST']}:{info.data['DB_PORT']}",
            path=f"{info.data['DB_NAME'] or ''}",
        ))


setting = Settings()