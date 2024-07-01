"""Get LLM to perform different tasks"""

from transformers import AutoTokenizer, AutoModelForCausalLM

from book_summarizer.config.config import setting

def get_llm_and_tokenizer(model_name: str=setting.LLM_MODEL_NAME) -> tuple[object, object]:
  """Get LLM and tokenizer"""

  tokenizer = AutoTokenizer.from_pretrained(model_name)
  model = AutoModelForCausalLM.from_pretrained(model_name)
  return tokenizer, model