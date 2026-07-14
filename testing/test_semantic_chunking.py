from app.services.semantic_chunk_service import create_semantic_chunks

paragraphs = [

"""
Data Mining is used to discover patterns in data.
""",

"""
Applications of Data Mining include fraud detection and market analysis.
""",

"""
Classification is a supervised learning algorithm.
""",

"""
Classification predicts labels for new records.
"""
]

chunks = create_semantic_chunks(paragraphs)

print("\nTOTAL CHUNKS:", len(chunks))

for i, chunk in enumerate(chunks):

    print("\n=================")
    print("CHUNK", i+1)
    print(chunk)