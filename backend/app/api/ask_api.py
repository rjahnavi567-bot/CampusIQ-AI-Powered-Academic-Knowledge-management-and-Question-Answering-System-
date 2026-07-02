from fastapi import APIRouter
import re

from app.services.hybrid_retrieval_service import hybrid_retrieve
from app.services.reranker_service import rerank_results
from app.services.context_builder import build_context
from app.services.groq_service import generate_answer
from app.database.connection import SessionLocal
from app.database.models import QuestionHistory
from app.schemas.ask_schema import AskRequest
from app.database.models import DocumentImage
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
    print("\n========== ASK REQUEST ==========")
    print("Question :", question)
    print("Selected File :", source_file)
    print("Selected Page :", page_no)
    print("=================================\n")

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
    # -------------------------------------
# Extract diagrams/images
# -------------------------------------
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

    # ----------------------------------------
    # Parse USED_IMAGES
    # ----------------------------------------

    used_ids = []

    match = re.search(

    r"USED_IMAGES:(.*)",

    answer,

    re.DOTALL

)

    if match:

        lines = match.group(1).strip().splitlines()

        for line in lines:

            line = line.strip()

            if re.fullmatch(r"[a-f0-9]{8}", line):
                used_ids.append(line)

    # Remove USED_IMAGES section from answer

    answer = re.sub(

    r"USED_IMAGES:.*",

    "",

    answer,

    flags=re.DOTALL

).strip()

    # =====================================
    # FETCH ALL RELEVANT DIAGRAMS
    # =====================================

    db = SessionLocal()

    relevant_images = []
    seen = set()

    try:

      if used_ids:

        images = (
            db.query(DocumentImage)
            .filter(DocumentImage.image_hash.in_(used_ids))
            .all()
        )

        for img in images:

            if img.image_hash in seen:
                continue

            seen.add(img.image_hash)

            relevant_images.append({
                "title": img.title,
                "caption": img.caption,
                "page_no": img.page_no,
                "image_path": img.image_path
            })
      else:

        seen=set()

        for chunk in top_chunks:

            meta=chunk["metadata"]

            if meta.get("type")!="image":
                continue

            path=meta.get("image_path")

            if path in seen:
                continue

            seen.add(path)

            relevant_images.append({

            "title":meta.get("title","Diagram"),

            "caption":meta.get("caption",""),

            "page_no":meta.get("page_no"),

            "image_path":path

        })

    finally:

            db.close()

    relevant_images.sort(
    key=lambda x: x["page_no"]
)

    # =====================================
    # AI CONFIDENCE SCORE
    # =====================================

    retrieval_score = 0
    reranker_score = 0
    coverage_score = 0
    image_score = 0 

    # ------------------------------
    # Retrieval Quality (30%)
    # ------------------------------

    if scores:

        avg_distance = sum(scores) / len(scores)

        retrieval_score = max(

        0,

        min(

            100,

            (1 - avg_distance) * 100

        )

    )

# ------------------------------
# CrossEncoder Quality (40%)
# ------------------------------

    if ranked:

        top_scores = [

        item["score"]

        for item in ranked[:5]

    ]

        avg_cross = sum(top_scores) / len(top_scores)

    # CrossEncoder scores usually lie around
    # -5 to +15

        reranker_score = max(

        0,

        min(

            100,

            ((avg_cross + 5) / 20) * 100

        )

    )

# ------------------------------
# Evidence Coverage (20%)
# ------------------------------

    coverage_score = min(

    100,

    len(top_chunks) * 16.7

)

# ------------------------------
# Diagram Usage (10%)
# ------------------------------

    if len(relevant_images):

            image_score = min(

        100,

        len(relevant_images) * 25

    )

# ------------------------------
# Final Confidence
# ------------------------------

    confidence = round(

    retrieval_score * 0.30 +

    reranker_score * 0.40 +

    coverage_score * 0.20 +

    image_score * 0.10,

    2

)
    print("\n===== CONFIDENCE =====")

    print("Retrieval :", round(retrieval_score,2))

    print("Reranker :", round(reranker_score,2))

    print("Coverage :", round(coverage_score,2))

    print("Images :", round(image_score,2))

    print("Final :", confidence)

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
    print(source_file)

    return {

    "question": question,

    "answer": answer,

    "marks": marks,

    "confidence": confidence,

    "sources": [

        {

            "file": chunk["metadata"].get("source_file"),

            "page": chunk["metadata"].get("page_no"),

            "type": chunk["metadata"].get("type", "text")

        }

        for chunk in top_chunks

    ],

    "images": relevant_images

}