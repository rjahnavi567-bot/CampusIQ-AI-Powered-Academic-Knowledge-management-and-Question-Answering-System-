from fastapi import APIRouter

from app.services.retrieval.hybrid_retrieval_service import hybrid_retrieve
from app.services.reranker_service import rerank_results
from app.services.statistics import collector
from app.services.statistics.timer import Timer
from app.services.retrieval.confidence_validator import (
    validate_retrieval
)
from fastapi import Depends
from app.dependencies.auth_dependency import get_current_user
router = APIRouter()


@router.get("/search")
def search(
    query: str,
    source_file: str = None
):
  try:
    # ---------------------------------
    # Statistics Timers
    # ---------------------------------
    search_timer = Timer()
    search_timer.start()

    collector.increment("Total Search Queries Executed")

    # ---------------------------------
    # Hybrid Retrieval
    # ---------------------------------

    documents, metadatas, scores = hybrid_retrieve(
        question=query,
        source_file=source_file,
        top_k=20
    )
    

    collector.increment(
    "Total Retrieved Chunks",
    len(documents)
)

    print("Retrieved Results :", len(documents))
    

    # ---------------------------------
    # Cross Encoder Re-ranking
    # ---------------------------------

    ranked = rerank_results(
        query,
        documents,
        metadatas
    )
    collector.increment(
    "Top-10 Retrieval Accuracy",
    min(10, len(ranked))
)

    collector.increment(
    "Top-5 Retrieval Accuracy",
    min(5, len(ranked))
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
    # ---------------------------------
# Confidence Validation
# ---------------------------------

    is_confident, top_score = validate_retrieval(ranked)

    if not is_confident:

        return {
        "query": query,
        "total_retrieved": len(documents),
        "confidence": top_score,
        "results": [],
        "message":
            "The uploaded academic resources do not contain sufficient information to answer this question."
    }
    if len(ranked) > 0:
        print("Top Score :", ranked[0]["score"])

    # ---------------------------------
    # Build Response
    # ---------------------------------

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

            "retrieval_type": item["metadata"].get(
                "retrieval_type",
                "text"
            ),

            "similarity_score": item["metadata"].get(
                "similarity_score",
                0
            )

        })

    # ---------------------------------
    # Summary
    # ---------------------------------

    print("\n==============================")
    print("SEARCH API SUMMARY")
    print("==============================")

    text_count = sum(
        1 for x in top_results
        if x["retrieval_type"] == "text"
    )

    image_count = sum(
        1 for x in top_results
        if x["retrieval_type"] == "image"
    )

    print("Text Results :", text_count)
    print("Image Results:", image_count)
    print("==============================")
    search_time = search_timer.stop()

    collector.timer(
    "Semantic Search Time",
    search_time
)

    collector.increment(
    "Total Successful Searches"
)

    return {

        "query": query,

        "total_retrieved": len(documents),

        "results": top_results

    }
  except Exception:
     collector.increment("Total Failed Searches")
     raise