from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    local_files_only=True
)


def rerank_results(
    query,
    documents,
    metadatas
):

    query_embedding = model.encode(
        query,
        convert_to_tensor=True
    )

    doc_embeddings = model.encode(
        documents,
        convert_to_tensor=True
    )

    similarities = cos_sim(
        query_embedding,
        doc_embeddings
    )[0]

    ranked = []

    for doc, metadata, score in zip(
        documents,
        metadatas,
        similarities
    ):

        ranked.append({
            "content": doc,
            "metadata": metadata,
            "score": float(score),

            # IMPORTANT
            "source_file": metadata.get(
                "source_file",
                "Unknown"
            ),

            "page_no": metadata.get(
                "page_no",
                "Unknown"
            ),

            "similarity_score": metadata.get(
                "similarity_score",
                0
            )
        })

    ranked.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked