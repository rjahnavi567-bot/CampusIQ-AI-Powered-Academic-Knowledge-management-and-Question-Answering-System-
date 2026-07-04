from app.services.chroma_service import text_collection


def store_text_chunks(document_id, chunks):
    """
    Store all semantic text chunks into ChromaDB
    using a single bulk insert.
    """

    if not chunks:
        print("No chunks to store.")
        return

    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):

        ids.append(f"{document_id}_{i}")

        documents.append(
            chunk.get("content", "")
        )

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

        if (
            "file_type" in chunk
            and chunk["file_type"] is not None
        ):
            metadata["file_type"] = chunk["file_type"]

        metadatas.append(metadata)

    text_collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    print(
        f"Stored {len(chunks)} text chunks."
    )