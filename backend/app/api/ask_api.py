from fastapi import APIRouter
import re

from app.services.hybrid_retrieval_service import hybrid_retrieve
from app.services.reranker_service import rerank_results
from app.services.context_builder import build_context
from app.services.groq_service import generate_answer

from app.database.connection import SessionLocal
from app.database.models import QuestionHistory
from app.schemas.ask_schema import AskRequest

router = APIRouter()


@router.post("/ask")
def ask(request: AskRequest):

    question = request.question
    marks = request.marks

    # =====================================
    # PAGE FILTER
    # =====================================

    page_match = re.search(
        r"page\s+(\d+)",
        question.lower()
    )

    page_no = None

    if page_match:
        page_no = int(page_match.group(1))

    # =====================================
    # DOCUMENT FILTER
    # =====================================

    source_file = None

    if request.documents:

        # currently search first selected file
        # later we will improve multi-document search

        source_file = request.documents[0]

    # =====================================
    # RETRIEVE
    # =====================================

    documents, metadatas, scores = hybrid_retrieve(

    question=question,

    page_no=page_no,

    source_file=source_file,

    top_k=10

)

    print("\n========== HYBRID RESULTS ==========\n")

    for doc, meta in zip(documents, metadatas):

        print("TYPE:", meta.get("type", "text"))
        print("PAGE:", meta.get("page_no"))
        print("FILE :", meta.get("source_file"))
        print(doc[:200])
        print("--------------------------------")

    # =====================================
    # NO RESULTS
    # =====================================

    if len(documents) == 0:

        return {

            "question": question,

            "answer": "No relevant content found.",

            "sources": []

        }

    # =====================================
    # RERANK
    # =====================================

    ranked = rerank_results(

        question,

        documents,

        metadatas

    )

    # =====================================
    # PAGE PRIORITY
    # =====================================

    if page_no is not None:

        ranked.sort(

            key=lambda x: (

                x["metadata"].get("page_no") == page_no,

                x["metadata"].get("type") == "image",

                x["score"]

            ),

            reverse=True

        )

    # =====================================
    # TOP CHUNKS
    # =====================================

    top_chunks = ranked[:6]
    # =====================================
# Separate image and text chunks
# =====================================

    image_chunks = [
    chunk
    for chunk in top_chunks
    if chunk["metadata"].get("type") == "image"
]

    text_chunks = [
    chunk
    for chunk in top_chunks
    if chunk["metadata"].get("type") != "image"
]

# Mix both text and image context
    combined_chunks = []

    text_index = 0
    image_index = 0

    while (
    text_index < len(text_chunks)
    or image_index < len(image_chunks)
):

      if text_index < len(text_chunks):
        combined_chunks.append(text_chunks[text_index])
        text_index += 1

      if image_index < len(image_chunks):
        combined_chunks.append(image_chunks[image_index])
        image_index += 1

    context = build_context(combined_chunks)

    print("\n========== CONTEXT ==========\n")

    print(context)

    # =====================================
    # GENERATE ANSWER
    # =====================================
    print("\n========== FINAL CONTEXT ==========\n")
    print(context)
    answer = generate_answer(

        question,

        context,

        marks

    )

    # =====================================
    # CONFIDENCE
    # =====================================

    confidence = 0

    if len(scores):

        avg = sum(scores) / len(scores)

        confidence = round(

            max(

                0,

                min(

                    100,

                    (1 / (1 + avg)) * 100

                )

            ),

            2

        )

    # =====================================
    # SAVE HISTORY
    # =====================================

    db = SessionLocal()

    try:

        history = QuestionHistory(

            question=question,

            answer=answer,

            document_name=", ".join(request.documents)

            if request.documents

            else "All Documents"

        )

        db.add(history)

        db.commit()

    finally:

        db.close()

    # =====================================
    # RESPONSE
    # =====================================

    return {

        "question": question,

        "answer": answer,

        "marks": marks,

        "confidence": confidence,

        "sources": [

            {

                "file":

                    chunk["metadata"].get(

                        "source_file"

                    ),

                "page":

                    chunk["metadata"].get(

                        "page_no"

                    ),

                "type":

                    chunk["metadata"].get(

                        "type",

                        "text"

                    )

            }

            for chunk in top_chunks

        ]

    }