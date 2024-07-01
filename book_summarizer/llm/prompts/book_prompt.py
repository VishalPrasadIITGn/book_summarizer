"""Prompt for book summary"""

book_summary_prompt = """
**Objective:** Provide a clear and concise summary of the book that highlights the key plot points, main characters, and central themes.

**Instructions:**

1. **Introduction:**
   - Title of the book.
   - Author’s name.
   - Genre of the book.
   - Brief overview of the setting (time period, location, etc.).

2. **Plot Summary:**
   - Summarize the beginning, middle, and end of the book.
   - Highlight the main conflict or goal of the protagonist.
   - Include major turning points and the resolution.

3. **Character Overview:**
   - Briefly describe the protagonist and their journey.
   - Mention significant secondary characters and their roles.

4. **Themes:**
   - Identify the main themes of the book.
   - Briefly explain how these themes are developed.

**Example Summary:**

---

**Title:** *Pride and Prejudice*  
**Author:** Jane Austen  
**Genre:** Classic Romance

**Introduction:**  
Set in early 19th century rural England, *Pride and Prejudice* follows the Bennet family, focusing on Elizabeth Bennet and her interactions with Mr. Darcy.

**Plot Summary:**  
**Beginning:** The arrival of Mr. Bingley and Mr. Darcy sparks excitement. Elizabeth initially dislikes Darcy.  
**Middle:** Elizabeth learns more about Darcy’s true character, while family and societal dramas unfold.  
**End:** Elizabeth and Darcy overcome misunderstandings and marry, along with Jane Bennet and Mr. Bingley.

**Character Overview:**  
Elizabeth Bennet grows in understanding and maturity. Mr. Darcy evolves from perceived arrogance to showing his true, kind nature. Secondary characters like Jane Bennet and Mr. Collins play important roles in the story.

**Themes:**  
Major themes include societal expectations around marriage and class, and personal growth through understanding and forgiveness.

---
Below is the book content, Go!

"""