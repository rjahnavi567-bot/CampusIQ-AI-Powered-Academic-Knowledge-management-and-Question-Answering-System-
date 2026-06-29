from app.services.chroma_service import text_collection


def store_text_chunks(document_id, chunks):
    """
    Store semantic text chunks into Text ChromaDB.
    """

    for i, chunk in enumerate(chunks):

        text_collection.add(

            ids=[
                f"{chunk['source_file']}_{i}"
            ],

            documents=[
                chunk["content"]
            ],

            metadatas=[
                {
                    "document_id": document_id,
                    "type": "text",
                    "topic": chunk["topic"],
                    "keywords": ",".join(
                        chunk.get("keywords", [])
                    ),
                    "source_file": chunk["source_file"],
                    "file_type": chunk.get("file_type"),
                    "page_no": chunk.get("page_no", 1),
                    "similarity_score": chunk.get(
                        "similarity_score",
                        0
                    )
                }
            ]
        )

    print(f"Stored {len(chunks)} text chunks.")