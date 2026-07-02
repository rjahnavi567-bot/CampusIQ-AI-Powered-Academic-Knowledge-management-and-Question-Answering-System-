from sentence_transformers import CrossEncoder

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def image_bonus(metadata):
    """
    Give image chunks extra score.

    This makes diagrams survive reranking
    if they are even slightly relevant.
    """

    bonus = 0

    if metadata.get("type") == "image":
        bonus += 0.80

    title = metadata.get("title", "").lower()

    important_words = [

        "diagram",

        "flowchart",

        "architecture",

        "block",

        "graph",

        "chart",

        "table",

        "algorithm",

        "process",

        "model",

        "structure"

    ]

    if any(word in title for word in important_words):
        bonus += 0.40

    return bonus


def rerank_results(question, documents, metadatas):

    if len(documents) == 0:
        return []

    pairs = [

        [question, doc]

        for doc in documents

    ]

    scores = reranker.predict(pairs)

    ranked = []

    for doc, meta, score in zip(

        documents,

        metadatas,

        scores

    ):

        final_score = float(score) + image_bonus(meta)

        ranked.append({

            "content": doc,

            "metadata": meta,

            "score": final_score,

            "cross_score": float(score)

        })

    ranked.sort(

        key=lambda x: x["score"],

        reverse=True

    )

    print("\n=========== FINAL RANK ===========")

    for item in ranked:

        print(

            round(item["score"], 2),

            "(cross:", round(item["cross_score"], 2), ")",

            item["metadata"].get("type"),

            item["metadata"].get("title", ""),

            "page",

            item["metadata"].get("page_no")

        )

    print("==================================\n")

    return ranked