from app.services.chunk_service import create_semantic_chunks

text = """
Data Mining is the process of discovering patterns in data.
Classification is a supervised learning technique.
Clustering groups similar objects together.

Artificial Intelligence enables machines to learn and reason.
"""

chunks = create_semantic_chunks(text)

for i, chunk in enumerate(chunks):
    print(f"\nCHUNK {i+1}")
    print("TOPIC:", chunk["topic"])
    print("CONTENT:", chunk["content"])