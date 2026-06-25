from app.services.semantic_chunker import create_semantic_chunks

paragraphs = [
    "Machine Learning is AI",

    "Supervised Learning is a type of Machine Learning",

    "Databases store data",

    "Normalization improves databases"
]

chunks = create_semantic_chunks(paragraphs)

for chunk in chunks:
    print("==========")
    print(chunk)