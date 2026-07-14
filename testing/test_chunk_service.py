from app.services.chunk_service import create_semantic_chunks

text = """
Data Mining is the process of discovering patterns in data.

Classification is a supervised learning technique.

Clustering groups similar objects together.
"""

chunks = create_semantic_chunks(text)

print("Number of chunks:", len(chunks))

for chunk in chunks:
    print(chunk)