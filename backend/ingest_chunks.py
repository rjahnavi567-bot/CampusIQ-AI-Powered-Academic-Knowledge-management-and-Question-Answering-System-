from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import create_semantic_chunks
from app.services.chroma_service import text_collection

pdf_path = "data mining book.pdf"

text = extract_text_from_pdf(pdf_path)

chunks = create_semantic_chunks(text)

for i, chunk in enumerate(chunks):

    text_collection.add(
        ids=[f"chunk_{i}"],
        documents=[chunk["content"]],
        metadatas=[
            {
                "topic": chunk["topic"],
                "source": pdf_path,
                "chunk_number": i
            }
        ]
    )
print(f"{len(chunks)} chunks stored in ChromaDB.")