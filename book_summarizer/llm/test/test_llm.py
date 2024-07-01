import unittest
from unittest.mock import patch, MagicMock

from book_summarizer.llm.get_llm import get_llm_and_tokenizer
from book_summarizer.llm.prompts.book_prompt import book_summary_prompt
from book_summarizer.config.config import setting
from book_summarizer.llm.llm_summarize import get_llm_output, get_content_summary


class TestBookSummarizer(unittest.TestCase):
  
    def setup_class(cls) -> None:
      """Setup class for test cases"""
      cls.llm_model_name=setting.LLM_MODEL_NAME
      cls.llm_prompt=setting.LLM_PROMPT
      cls.book_content = "This is a story about a fictional fairy"
      cls.question = "Answer this question in 10 words or more: How many days in a week?"

    def test_get_llm_output(self) -> None:
        """Test get llm output function"""

        result = get_llm_output(llm_input=self.question, model_name=self.llm_model_name)

        assert result
        assert len(result)>10
        print(result)
        assert "day" in result.lower()

    def test_get_content_summary(self):
        """Tets content summary"""

        summary = get_content_summary(content=self.book_content, model_name=self.llm_model_name, prompt_name=self.llm_prompt)
        assert summary
        assert len(summary)>200
        assert all([keyword in summary.lower() for keyword in ["title", "summary", "genre"]])

# if __name__ == "__main__":
#     unittest.main()
