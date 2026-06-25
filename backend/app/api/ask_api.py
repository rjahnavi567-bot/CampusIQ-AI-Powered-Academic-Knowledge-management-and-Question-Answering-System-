from fastapi import APIRouter

from app.services.chroma_service import collection
from app.services.reranker_service import rerank_results
from app.services.context_builder import build_context
from app.database.models import QuestionHistory
from app.schemas.ask_schema import AskRequest
from app.database.connection import SessionLocal
from app.services.groq_service import generate_answer

router = APIRouter()


@router.post("/ask")
def ask(request: AskRequest):

    question = request.question
    marks = request.marks

    # ====================================
    # SEARCH IN ALL DOCUMENTS
    # ====================================
    if not request.documents:

        results = collection.query(
            query_texts=[question],
            n_results=5
        )

    # ====================================
    # SEARCH ONLY SELECTED DOCUMENTS
    # ====================================
    else:

        all_docs = []
        all_metadatas = []
        all_distances = []

        for filename in request.documents:

            partial = collection.query(
                query_texts=[question],
                n_results=5,
                where={
                    "source_file": filename
                }
            )

            all_docs.extend(
                partial.get("documents", [[]])[0]
            )

            all_metadatas.extend(
                partial.get("metadatas", [[]])[0]
            )

            all_distances.extend(
                partial.get("distances", [[]])[0]
            )

        results = {
            "documents": [all_docs],
            "metadatas": [all_metadatas],
            "distances": [all_distances]
        }

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    scores = results.get(
        "distances",
        [[]]
    )[0]

    # ====================================
    # NO RESULTS
    # ====================================
    if not documents:

        return {
            "question": question,
            "answer":
            "No relevant content found in selected document(s).",
            "sources": []
        }

    # ====================================
    # CONFIDENCE
    # ====================================
    confidence = 0

    if scores:

        avg_distance = (
    sum(scores) / len(scores)
)

        confidence = max(
    0,
    min(
        100,
        round((1 / (1 + avg_distance)) * 100)
    )
)

    # ====================================
    # RERANK
    # ====================================
    ranked = rerank_results(
        question,
        documents,
        metadatas
    )

    top_chunks = ranked[:2]

    context = build_context(
        top_chunks
    )

    print(
        "CONTEXT LENGTH:",
        len(context)
    )

    # ====================================
    # GENERATE ANSWER
    # ====================================
    ai_answer = generate_answer(
        question,
        context,
        marks
    )

    # ====================================
    # SAVE QUESTION HISTORY
    # ====================================
    db = SessionLocal()

    try:

        selected_docs = ", ".join(
    request.documents
) if request.documents else "All Documents"

        history = QuestionHistory(
    question=question,
    answer=ai_answer,
    document_name=selected_docs
)

        db.add(history)
        db.commit()

    finally:

        db.close()

    # ====================================
    # RESPONSE
    # ====================================
    return {
        "question": question,
        "answer": ai_answer,
        "marks": marks,
        "confidence": round(
            confidence,
            2
        ),
        "sources": [
            {
                "file":
                chunk["metadata"].get(
                    "source_file"
                ),
                "page":
                chunk["metadata"].get(
                    "page_no"
                )
            }
            for chunk in top_chunks
        ]
    }