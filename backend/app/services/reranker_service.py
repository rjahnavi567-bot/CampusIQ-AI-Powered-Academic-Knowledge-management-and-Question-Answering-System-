from sentence_transformers import CrossEncoder

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank_results(
    question,
    documents,
    metadatas
):
    """
    Rerank retrieved chunks using CrossEncoder.
    """

    if len(documents) == 0:
        return []

    pairs = []

    for doc in documents:
        pairs.append(
            [question, doc]
        )

    scores = reranker.predict(
        pairs
    )

    ranked = []

    for doc, meta, score in zip(
        documents,
        metadatas,
        scores
    ):

        ranked.append(
            {
                "content": doc,
                "metadata": meta,
                "score": float(score)
            }
        )

    ranked.sort(
        key=lambda x: x["score"],
        reverse=True
    )
    print("\n===== RERANK RESULTS =====")

    for item in ranked:

      print(
        round(item["score"], 2),
        item["metadata"].get("page_no"),
        item["metadata"].get("type"),
        item["content"][:80]
    )

    return ranked