from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_answer(question, context, marks):

    prompt = f"""
You are an Academic Answer Generator.

Question:
{question}

Context:
{context}

Marks:
{marks}

Rules:

If marks = 2:
- Maximum 100 words
- One sentence introduction
- 2 bullet points

If marks = 5:
- Short introduction
- Exactly 5 bullet points
- One line conclusion
- Maximum 250 words

If marks = 10:
- Detailed introduction
- Exactly 8 bullet points
- Conclusion
- Maximum 400 words

Important:
- Use ONLY the given context.
- Do NOT mention source files.
- Do NOT say "according to context".
- Make answer easy for students to remember.
- Use bullet points.
- Use headings:
  Introduction
  Key Points
  Conclusion

When IMAGE sections are present:

1. Treat IMAGE sections exactly like textbook figures.

2. Read TITLE before CAPTION.

3. Use OCR only when useful.

4. Explain every diagram you actually used.

5. Never ignore retrieved diagrams.

6. At the END of your answer output exactly:

USED_IMAGES:
hash1
hash2
hash3

Replace hash1, hash2... with the image_hash values of every diagram you actually used.

If no diagram was used:

USED_IMAGES:
NONE

Never invent hashes.

Never output hashes inside the answer body.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=500
    )

    return response.choices[0].message.content