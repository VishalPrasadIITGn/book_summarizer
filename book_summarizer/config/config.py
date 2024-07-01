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

  CLM_URL: str = "http://10.113.34.11:8999"
  REDIS_HOST: str = "10.113.34.11"
  REDIS_PORT: int = 6886
  REDIS_PASSWORD: str = ""
  REDIS_URL: str = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"
  OPENAI_COMPLETIONS_ENGINE: str = "gpt-3.5-turbo"
  UPLOAD_PATH: str = f"uploaded_docs"
  # LLM_MODEL_NAME: str="meta-llama/Meta-Llama-3-8B-Instruct"
  LLM_MODEL_NAME: str = "microsoft/Phi-3-mini-128k-instruct"
  LLM_PROMPT: str = book_summary_prompt

  LRU_CACHE_SIZE: int = 3

  DB_USERNAME: str = os.getenv("DB_USERNAME") or "user"
  DB_PASSWORD: str = os.getenv("DB_PASSWORD") or "password123"
  DB_NAME: str = "book_rec_2"

  DB_HOST: str = "10.113.34.11"
  DB_PORT: int = 8765
  DB_SCHEME: str = "postgresql"
  SQLALCHEMY_DATABASE_URL: PostgresDsn | None = "postgresql://user:password123@10.113.34.11:8765/book_rec_2"

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
#confi =Settings()
# print("DB_USERNAME : ",setting.DB_USERNAME)
# print("DB_PASSWORD : ",setting.DB_PASSWORD)
# print("DB_PORT : ",setting.DB_PORT)
# print("DB_SCHEME : ",setting.DB_SCHEME)
# print("DB_HOST : ",setting.DB_HOST)

# redis_cache = {
#     "uploaded_docs":
#     redis.StrictRedis( # type: ignore
#         host=setting.REDIS_HOST,
#         port=setting.REDIS_PORT,
#         password=setting.REDIS_PASSWORD,
#         decode_responses=True,
#         db=1,
#     ),
#     "lease_data":
#     redis.StrictRedis( # type: ignore
#         host=setting.REDIS_HOST,
#         port=setting.REDIS_PORT,
#         password=setting.REDIS_PASSWORD,
#         decode_responses=True,
#         db=2,
#     ),
#     "parsed_results":
#     redis.StrictRedis( # type: ignore
#         host=setting.REDIS_HOST,
#         port=setting.REDIS_PORT,
#         password=setting.REDIS_PASSWORD,
#         decode_responses=True,
#         db=3,
#     ),
#     "document_qa":
#     redis.StrictRedis( # type: ignore
#         host=setting.REDIS_HOST,
#         port=setting.REDIS_PORT,
#         password=setting.REDIS_PASSWORD,
#         decode_responses=True,
#         db=4,
#     ),
#     "prompts":
#     redis.StrictRedis( # type: ignore
#         host=setting.REDIS_HOST,
#         port=setting.REDIS_PORT,
#         password=setting.REDIS_PASSWORD,
#         decode_responses=True,
#         db=5,
#     ),
#     "document_qa_user":
#     redis.StrictRedis( # type: ignore
#         host=setting.REDIS_HOST,
#         port=setting.REDIS_PORT,
#         password=setting.REDIS_PASSWORD,
#         decode_responses=True,
#         db=6,
#     ),
#     "lru_cache":
#     redis.StrictRedis( # type: ignore
#         host=setting.REDIS_HOST,
#         port=setting.REDIS_PORT,
#         password=setting.REDIS_PASSWORD,
#         decode_responses=False,
#         db=7,
#     ),
#     "lease_summary_data":
#     redis.StrictRedis( # type: ignore
#         host=setting.REDIS_HOST,
#         port=setting.REDIS_PORT,
#         password=setting.REDIS_PASSWORD,
#         decode_responses=True,
#         db=8,
#     ),
#     "invoice_data":
#     redis.StrictRedis( # type: ignore
#         host=setting.REDIS_HOST,
#         port=setting.REDIS_PORT,
#         password=setting.REDIS_PASSWORD,
#         decode_responses=True,
#         db=8,
#     ),
#     "reconciliation_history":
#     redis.StrictRedis( # type: ignore
#         host=setting.REDIS_HOST,
#         port=setting.REDIS_PORT,
#         password=setting.REDIS_PASSWORD,
#         decode_responses=True,
#         db=9,
#     ),
# }
