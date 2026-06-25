from app.services.embedding_service import generate_embedding

text = "Machine Learning is a subset of AI"

embedding = generate_embedding(text)

print(type(embedding))
print(len(embedding))