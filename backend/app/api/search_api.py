from fastapi import APIRouter

from app.services.chroma_service import text_collection
from app.services.reranker_service import rerank_results

router = APIRouter()


@router.get("/search")
def search(
    query: str,
    source_file: str = None
):

    # Search all documents
    if source_file is None:

        results = collection.query(
            query_texts=[query],
            n_results=10
        )

    # Search specific document only
    else:

        results = text_collection.query(
            query_texts=[query],
            n_results=20,
            where={
                "source_file": source_file
            }
        )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    print("Retrieved Docs:", len(documents))

    ranked = rerank_results(
        query,
        documents,
        metadatas
    )
    query_lower = query.lower()

    for item in ranked:

        topic = item["metadata"].get(
        "topic",
        ""
    ).lower()

        if any(
            word in topic
            for word in query_lower.split()
    ):
            item["score"] += 0.20
    ranked.sort(
    key=lambda x: x["score"],
    reverse=True
)
    if len(ranked) > 0:
        print("Top Score:", ranked[0]["score"])

    top_results = []

    for item in ranked[:3]:

        top_results.append({
    "score": item["score"],
    "content": item["content"],
    "topic": item["metadata"].get(
        "topic",
        ""
    ),
    "source_file": item["metadata"].get(
        "source_file",
        ""
    ),
    "page_no": item["metadata"].get(
        "page_no",
        1
    ),
    "similarity_score":
        item["metadata"].get(
            "similarity_score",
            0
        )
})

    return {
        "query": query,
        "total_retrieved": len(documents),
        "results": top_results
    }