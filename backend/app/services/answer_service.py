def generate_answer(question, chunks):

    context = "\n\n".join(chunks)

    return f"""
Question:
{question}

Relevant Content:

{context}
"""