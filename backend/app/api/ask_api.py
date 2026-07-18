from fastapi import APIRouter
import re

from app.services.retrieval.hybrid_retrieval_service import (

    retrieve_text,

    retrieve_images


)
from app.services.statistics import collector
from app.services.statistics.timer import Timer
from app.services.reranker_service import rerank_results
from app.services.context_builder import build_context
from app.services.groq_service import generate_answer
from app.database.connection import SessionLocal
from app.database.models import QuestionHistory
from app.schemas.ask_schema import AskRequest
from app.database.models import DocumentImage
from app.services.image_embedding_service import (
    embed_text_for_image_search
)

from app.services.image_reranker_service import rerank_images
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

    # =====================================================
    # STEP 1 : Retrieve Text
    # =====================================================

    documents, metadatas, scores = retrieve_text(

    question=question,

    page_no=page_no,

    source_file=source_file,

    top_k=8

)

# =====================================================
# STEP 2 : Collect Relevant Pages
# =====================================================

    candidate_pages = set()

    for meta in metadatas:

        page = meta.get("page_no")

        if page is None:
            continue

        candidate_pages.add(page)

        candidate_pages.add(page - 1)

        candidate_pages.add(page + 1)

    candidate_pages = [

    p

    for p in candidate_pages

    if p >= 1

]

    print()

    print("Candidate Pages :", sorted(candidate_pages))

    print()

# =====================================================
# STEP 3 : Retrieve Images only from nearby pages
# =====================================================

    img_docs, img_meta, img_scores = retrieve_images(

    question=question,

    pages=candidate_pages,

    source_file=source_file,

    top_k=6

)

# =====================================================
# STEP 4 : Merge
# =====================================================

    documents.extend(img_docs)

    metadatas.extend(img_meta)

    scores.extend(img_scores)

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
# Collect pages of top text chunks
# =====================================

    important_pages = set()

    for chunk in top_chunks:

       if chunk["metadata"].get("type") != "image":

        important_pages.add(
            chunk["metadata"].get("page_no")
        )

    print("\nImportant Pages :", important_pages)
    # -------------------------------------
# Extract diagrams/images
# -------------------------------------
    # =====================================
# Separate image and text chunks
# =====================================

    image_chunks = []

    for chunk in ranked:

        meta = chunk["metadata"]

        if meta.get("type") != "image":
           continue

        if meta.get("page_no") in important_pages:

           image_chunks.append(chunk)

    print("Filtered Images :", len(image_chunks))
    print()

    print("Reranking Images...")

    image_chunks = rerank_images(

    question,

    image_chunks

)
    image_chunks = image_chunks[:2]

    print("Images after reranking :", len(image_chunks))

    print()

    text_chunks = [
    chunk
    for chunk in top_chunks
    if chunk["metadata"].get("type") != "image"
]
    # Sort image chunks by reranker score


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
    rag_timer = Timer()
    rag_timer.start()
    answer = generate_answer(

        question,

        context,

        marks

    )
    rag_time = rag_timer.stop()

    collector.increment("Total RAG Responses Generated")

    collector.add_time(
    "RAG Response Time",
    rag_time
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
    collector.increment("Total API Requests Processed")

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