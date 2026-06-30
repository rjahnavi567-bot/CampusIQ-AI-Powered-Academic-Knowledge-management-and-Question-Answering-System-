from app.services.chroma_service import text_collection


def store_text_chunks(document_id, chunks):
    """
    Store semantic text chunks into ChromaDB.
    """

    for i, chunk in enumerate(chunks):

        metadata = {
            "document_id": document_id,
            "type": "text",
            "topic": chunk.get("topic", ""),
            "keywords": ",".join(
                chunk.get("keywords", [])
            ),
            "source_file": chunk.get(
                "source_file",
                ""
            ),
            "page_no": int(
                chunk.get("page_no", 1)
            ),
            "similarity_score": float(
                chunk.get(
                    "similarity_score",
                    0
                )
            )
        }

        # Add file_type ONLY if it exists
        if (
            "file_type" in chunk
            and chunk["file_type"] is not None
        ):
            metadata["file_type"] = chunk["file_type"]

        text_collection.add(

            ids=[
                f"{document_id}_{i}"
            ],

            documents=[
                chunk.get("content", "")
            ],

            metadatas=[
                metadata
            ]
        )

    print(
        f"Stored {len(chunks)} text chunks."
    )