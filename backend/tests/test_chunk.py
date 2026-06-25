from app.services.chunk_service import create_semantic_chunks

text = """
Data Mining is used to discover patterns in data.

Applications of Data Mining include fraud detection and market analysis.

Classification is a supervised learning algorithm.

Classification predicts labels for new records.
"""

chunks = create_semantic_chunks(text)

print("\nTOTAL CHUNKS:", len(chunks))

for i, chunk in enumerate(chunks, start=1):

    print("\n=================")
    print("CHUNK", i)

    print("\nTOPIC:")
    print(chunk["topic"])

    print("\nCONTENT:")
    print(chunk["content"])

    print("\nKEYWORDS:")
    print(chunk["keywords"])