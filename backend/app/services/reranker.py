from sentence_transformers import CrossEncoder

model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank(query, documents):

    pairs = [
        (query, doc["content"])
        for doc in documents
    ]

    scores = model.predict(pairs)

    for doc, score in zip(documents, scores):
        doc["rerank_score"] = float(score)

    documents.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return documents