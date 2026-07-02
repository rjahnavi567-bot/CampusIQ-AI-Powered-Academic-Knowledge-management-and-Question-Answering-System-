from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_diagram_title(caption, ocr_text):
    """
    Generate a short academic title for a diagram.

    Example outputs:

    Computer System Block Diagram

    Bus Architecture

    Memory Hierarchy

    CPU Organization

    Cache Mapping
    """

    prompt = f"""
You are an academic assistant.

Generate ONLY a SHORT title (maximum 8 words).

Caption:
{caption}

OCR:
{ocr_text}

Rules:

Return only the title.

Do NOT explain.

Do NOT use quotes.

Good examples:

Computer System Block Diagram

Bus Architecture

Instruction Cycle

Memory Hierarchy

CPU Organization
"""

    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            temperature=0.1,

            max_tokens=20,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        title = response.choices[0].message.content.strip()

        title = title.replace("\n", " ")

        return title

    except Exception:

        return caption[:60]