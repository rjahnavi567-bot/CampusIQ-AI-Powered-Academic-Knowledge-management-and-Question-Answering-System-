from app.services.pdf_service import extract_text_from_pdf

from app.services.semantic_chunk_service import create_semantic_chunks

text = extract_text_from_pdf(
    "data mining book.pdf"
)

chunks = create_semantic_chunks(text)

for i, chunk in enumerate(chunks[:5]):

    print("\n====================")

    print("CHUNK:", i + 1)

    print("TOPIC:")
    print(chunk["topic"])

    print("\nCONTENT:")
    print(chunk["content"][:500])