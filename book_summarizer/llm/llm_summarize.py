from book_summarizer.llm.get_llm import get_llm_and_tokenizer
from book_summarizer.llm.prompts.book_prompt import book_summary_prompt
from book_summarizer.config.config import setting

def get_llm_output(llm_input: str, model_name: str=setting.LLM_MODEL_NAME) -> str:
    tokenizer, model = get_llm_and_tokenizer(model_name=model_name)
    inputs = tokenizer(llm_input, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=1000)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def get_content_summary(content: str, model_name: str=setting.LLM_MODEL_NAME, prompt_name: str=setting.LLM_PROMPT)-> str:
# Example usage
    llm_input = book_summary_prompt + "\n" + content
    summary = get_llm_output(llm_input=llm_input, model_name=model_name)
    return summary

if __name__ == "__main__":
    book_content = "Once there was a king"  # Your book content here
    summary = get_content_summary(book_content)
    print(summary)
