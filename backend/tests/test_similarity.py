from app.services.embedding_service import generate_embedding
from app.services.similarity_service import calculate_similarity

text1 = "Machine Learning is AI"

text2 = "Machine Learning is part of Artificial Intelligence"

vec1 = generate_embedding(text1)
vec2 = generate_embedding(text2)

score = calculate_similarity(vec1, vec2)

print(score)