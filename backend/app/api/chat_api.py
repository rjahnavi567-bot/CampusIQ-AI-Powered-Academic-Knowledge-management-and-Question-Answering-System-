from fastapi import APIRouter

from app.services.chroma_service import collection
from app.services.reranker_service import rerank_results
from app.services.context_builder import build_context
from app.services.gemini_service import generate_answer
router = APIRouter()


@router.get("/ask")
def ask(question: str):

    results = collection.query(
        query_texts=[question],
        n_results=10
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    ranked = rerank_results(
        question,
        documents,
        metadatas
    )

    top_results = []

    for item in ranked[:3]:

        top_results.append({
            "content": item["content"],
            "topic": item["metadata"].get(
                "topic",
                ""
            ),
            "source_file": item["metadata"].get(
                "source_file",
                ""
            )
        })

    context = build_context(
        top_results
    )

    answer = generate_answer(
    question,
    context
)

    return {
    "question": question,
    "answer": answer,
    "sources": [
        {
            "topic": item["topic"],
            "source_file": item["source_file"]
        }
        for item in top_results
    ]
}