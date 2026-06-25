from ollama import chat


class LLMService:

    def generate_answer(
        self,
        question: str,
        context: str,
        marks: int = 5
    ) -> str:

        prompt = f"""
You are an AI Academic Assistant.

Use ONLY the provided context.

If the answer cannot be found in the context,
reply:
'Information not found in provided material.'

Question:
{question}

Marks:
{marks}

Context:
{context}

Guidelines:

2 marks:
50-80 words

5 marks:
150-250 words

10 marks:
300-500 words

Answer:
"""

        response = chat(
            model="qwen3:8b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.message.content