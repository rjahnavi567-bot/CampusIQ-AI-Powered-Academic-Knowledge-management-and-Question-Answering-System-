import requests
import time

def generate_answer(question, context, marks):

    if marks <= 2:
        format_instruction = """
        Answer in this format:

        Introduction:
        One short sentence.

        Key Points:
        • 2 bullet points

        Maximum 60 words.
        """

    elif marks <= 5:
        format_instruction = """
        Answer in this format:

        Introduction:
        Short introduction.

        Key Points:
        • 5 bullet points

        Conclusion:
        One short sentence.
        """

    else:
        format_instruction = """
        Answer in this format:

        Introduction:
        Detailed introduction.

        Key Points:
        • 8 bullet points

        Conclusion:
        Summary sentence.
        """

    prompt = f"""
You are an academic assistant.

Use ONLY the provided context.

Question:
{question}

Context:
{context}

Marks: {marks}

Rules:

For 2 marks:
- One line introduction
- 2 bullet points

For 5 marks:
- One line introduction
- 5 bullet points
- One line conclusion

For 10 marks:
- One paragraph introduction
- 8 bullet points
- One paragraph conclusion

Keep answers concise.
Use bullet points.
Do not mention source files.
"""

    try:
        start = time.time()
        print("Sending to Ollama...")
        response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen3:4b",
            "prompt": prompt,
            "stream": False,
             "think": False
        },
        timeout=300
    )
        print("Time:", time.time() - start)
        print("Ollama finished.")

        return response.json()["response"]

    except Exception as e:
      return f"Model Error: {str(e)}"