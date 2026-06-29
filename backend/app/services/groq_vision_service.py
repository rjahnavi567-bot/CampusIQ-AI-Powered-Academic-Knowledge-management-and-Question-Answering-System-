import os
import base64

from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def image_to_base64(image_path):

    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def analyze_image(
    image_path,
    question=""
):
    """
    Uses Groq Vision model to understand diagrams.

    Returns a detailed explanation.
    """

    image_base64 = image_to_base64(image_path)

    response = client.chat.completions.create(

        model="meta-llama/llama-4-scout-17b-16e-instruct",

        messages=[
            {
                "role": "user",

                "content": [

                    {
                        "type": "text",

                        "text":

                        f"""
You are an engineering professor.

Analyze this image.

Question:
{question}

Explain every important diagram,
labels,
flow,
table,
graph,
block diagram,
architecture,
and equations.

Return a detailed explanation.
"""
                    },

                    {
                        "type": "image_url",

                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }

                ]
            }
        ]

    )

    return response.choices[0].message.content