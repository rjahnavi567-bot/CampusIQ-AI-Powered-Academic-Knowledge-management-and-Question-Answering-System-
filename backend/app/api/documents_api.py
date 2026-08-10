from fastapi import APIRouter, HTTPException
from app.database.connection import SessionLocal
from app.database.models import Document, Chunk
from app.services.chroma_service import text_collection
import os
import shutil
from app.services.document_cache import document_cache
from app.database.models import (
    Document,
    Chunk,
    DocumentImage
)
from app.services.trie_service import document_trie
from app.services.chroma_service import (
    text_collection,
    image_collection
)
from fastapi import Depends
from collections import defaultdict
from app.dependencies.auth_dependency import get_current_user

from collections import defaultdict

from collections import defaultdict

from fastapi import APIRouter, HTTPException, Depends
from app.services.document_processor import extract_text
from app.services.preview_service import build_preview_text
from app.services.subject_detection.subject_classifier import classify_subject
from app.services.chroma_service import text_collection
from app.database.connection import SessionLocal
from app.database.models import Document
from app.dependencies.auth_dependency import get_current_user

import json

router = APIRouter()


@router.post("/documents/reassign-subjects")
def reassign_old_document_subjects(
    current_user=Depends(get_current_user)
):
    db = SessionLocal()

    try:

        # --------------------------------------------------
        # Find documents uploaded before subject detection
        # --------------------------------------------------

        documents = (
            db.query(Document)
            .filter(
                (Document.subject == None) |
                (Document.subject == "")
            )
            .all()
        )

        print(
            f"\nFound {len(documents)} documents "
            f"without subjects."
        )

        results = []

        for document in documents:

            print("\n================================")
            print(
                f"Processing: {document.filename}"
            )
            print(
                f"Document ID: {document.id}"
            )
            print("================================")

            # --------------------------------------------------
            # Check file
            # --------------------------------------------------

            if not document.file_path:

                print("No file path. Skipping.")

                results.append({
                    "document_id": document.id,
                    "filename": document.filename,
                    "status": "skipped",
                    "reason": "No file path"
                })

                continue

            # --------------------------------------------------
            # Extract existing document text
            # --------------------------------------------------

            try:

                pages = extract_text(
                    document.file_path
                )

            except Exception as e:

                print(
                    "Text extraction failed:",
                    str(e)
                )

                results.append({
                    "document_id": document.id,
                    "filename": document.filename,
                    "status": "failed",
                    "reason": "Text extraction failed"
                })

                continue

            if not pages:

                print("No pages extracted.")

                results.append({
                    "document_id": document.id,
                    "filename": document.filename,
                    "status": "skipped",
                    "reason": "No text extracted"
                })

                continue

            # --------------------------------------------------
            # Build preview text
            # --------------------------------------------------

            try:

                preview_text = build_preview_text(
                    pages
                )

            except Exception as e:

                print(
                    "Preview generation failed:",
                    str(e)
                )

                results.append({
                    "document_id": document.id,
                    "filename": document.filename,
                    "status": "failed",
                    "reason": "Preview generation failed"
                })

                continue

            if not preview_text.strip():

                print("Empty preview text.")

                results.append({
                    "document_id": document.id,
                    "filename": document.filename,
                    "status": "skipped",
                    "reason": "Empty preview text"
                })

                continue

            # --------------------------------------------------
            # Existing subject detection pipeline
            # --------------------------------------------------

            try:

                subject_result = classify_subject(
                    preview_text
                )

            except Exception as e:

                print(
                    "Subject detection failed:",
                    str(e)
                )

                results.append({
                    "document_id": document.id,
                    "filename": document.filename,
                    "status": "failed",
                    "reason": "Subject detection failed"
                })

                continue

            print(
                "Detected subject:",
                subject_result
            )

            primary_subject = (
                subject_result.get(
                    "primary_subject"
                )
            )

            # --------------------------------------------------
            # No subject detected
            # --------------------------------------------------

            if not primary_subject:

                print(
                    "No subject detected. "
                    "Keeping document uncategorized."
                )

                results.append({
                    "document_id": document.id,
                    "filename": document.filename,
                    "status": "uncategorized"
                })

                continue

            # --------------------------------------------------
            # Update Document table
            # --------------------------------------------------

            document.subject = primary_subject

            document.primary_subject = (
                primary_subject
            )

            document.parent_subject = (
                subject_result.get(
                    "parent_subject",
                    ""
                )
            )

            document.subject_confidence = (
                subject_result.get(
                    "confidence",
                    0
                )
            )

            document.secondary_subjects = json.dumps(
                subject_result.get(
                    "secondary_subjects",
                    []
                )
            )

            document.matched_keywords = json.dumps(
                subject_result.get(
                    "matched_keywords",
                    []
                )
            )

            document.subject_detection_method = (
                subject_result.get(
                    "method",
                    "migration"
                )
            )

            document.subject_detected_by = (
                "Embedding Similarity v1"
            )

            db.commit()

            # --------------------------------------------------
            # Update ChromaDB metadata
            # --------------------------------------------------

            chroma_updated = 0

            try:

                chroma_results = text_collection.get()

                ids_to_update = []
                metadata_to_update = []

                for i, metadata in enumerate(
                    chroma_results.get(
                        "metadatas",
                        []
                    )
                ):

                    if not metadata:
                        continue

                    source_file = metadata.get(
                        "source_file"
                    )

                    if source_file != document.filename:
                        continue

                    updated_metadata = dict(
                        metadata
                    )

                    updated_metadata["subject"] = (
                        primary_subject
                    )

                    updated_metadata["parent_subject"] = (
                        subject_result.get(
                            "parent_subject",
                            ""
                        )
                    )

                    updated_metadata[
                        "subject_confidence"
                    ] = float(
                        subject_result.get(
                            "confidence",
                            0
                        )
                    )

                    secondary = (
                        subject_result.get(
                            "secondary_subjects",
                            []
                        )
                    )

                    updated_metadata[
                        "secondary_subjects"
                    ] = "|".join(
                        secondary
                    )

                    matched_keywords = (
                        subject_result.get(
                            "matched_keywords",
                            []
                        )
                    )

                    updated_metadata[
                        "matched_keywords"
                    ] = "|".join(
                        matched_keywords
                    )

                    updated_metadata[
                        "subject_detection_method"
                    ] = subject_result.get(
                        "method",
                        "migration"
                    )

                    ids_to_update.append(
                        chroma_results["ids"][i]
                    )

                    metadata_to_update.append(
                        updated_metadata
                    )

                if ids_to_update:

                    text_collection.update(
                        ids=ids_to_update,
                        metadatas=metadata_to_update
                    )

                    chroma_updated = len(
                        ids_to_update
                    )

                    print(
                        f"Updated {chroma_updated} "
                        "Chroma chunks."
                    )

            except Exception as e:

                print(
                    "Chroma metadata update failed:",
                    str(e)
                )

            # --------------------------------------------------
            # Result
            # --------------------------------------------------

            results.append({

                "document_id": document.id,

                "filename": document.filename,

                "status": "updated",

                "subject": primary_subject,

                "parent_subject": (
                    subject_result.get(
                        "parent_subject",
                        ""
                    )
                ),

                "confidence": (
                    subject_result.get(
                        "confidence",
                        0
                    )
                ),

                "method": (
                    subject_result.get(
                        "method",
                        "migration"
                    )
                ),

                "chroma_chunks_updated":
                    chroma_updated

            })

        return {

            "message":
                "Old document subject reassignment completed.",

            "total_documents_checked":
                len(documents),

            "results":
                results

        }

    finally:

        db.close()
@router.get("/documents/grouped")
def get_documents_grouped(
    current_user=Depends(get_current_user)
):
    db = SessionLocal()

    try:

        docs = (
            db.query(Document)
            .order_by(
                Document.parent_subject,
                Document.subject,
                Document.filename
            )
            .all()
        )

        grouped = defaultdict(list)

        for doc in docs:

            subject = (
                doc.subject
                if doc.subject
                else "Uncategorized"
            )

            grouped[subject].append(
                {
                    "id": doc.id,
                    "filename": doc.filename,
                    "subject": doc.subject,
                    "parent_subject": doc.parent_subject,
                    "status": doc.status,
                    "chunk_count": doc.chunk_count,
                    "created_at": doc.created_at
                }
            )

        # Convert dictionary into frontend-friendly list

        result = []

        for subject, documents in grouped.items():

            result.append(
                {
                    "subject": subject,
                    "documents": documents
                }
            )

        return result

    finally:
        db.close()
@router.get("/documents/suggestions")
def autocomplete(query: str):

    if not query:

        return []

    return document_trie.search_prefix(query)
@router.get("/documents/search")
def search_documents(query: str):

    if not query.strip():
        return []

    # 1. Exact search using HashMap
    exact = document_cache.get_document(query)

    if exact:
        return [exact]

    # 2. Partial search using PostgreSQL
    db = SessionLocal()

    try:

        documents = (
            db.query(Document)
            .filter(Document.filename.ilike(f"%{query}%"))
            .order_by(Document.filename)
            .all()
        )

        return documents

    finally:
        db.close()
# ==========================
# GET ALL DOCUMENTS
# ==========================

@router.get("/documents")
def get_documents(
    current_user=Depends(get_current_user)
):
    db = SessionLocal()

    try:

        docs = (
            db.query(Document)
            .order_by(Document.filename)
            .all()
        )

        return docs

    finally:
        db.close()


# ==========================
# VIEW DOCUMENT URL
# ==========================

@router.get("/documents/{document_id}/view")
def view_document(document_id: int):

    db = SessionLocal()

    try:

        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if not document:

            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )

        return {
            "filename": document.filename,
            "url":
f"http://localhost:8000/{document.file_path}"
        }

    finally:
        db.close()


# ==========================
# GET SINGLE DOCUMENT
# ==========================

@router.get("/documents/{document_id}")
def get_document(document_id: int):

    db = SessionLocal()

    try:

        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if not document:

            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )

        return document

    finally:
        db.close()


@router.get(
    "/documents/{document_id}/page/{page_no}"
)
def open_document_page(
    document_id: int,
    page_no: int
):

    db = SessionLocal()

    try:

        document = (
            db.query(Document)
            .filter(
                Document.id == document_id
            )
            .first()
        )

        if not document:

            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )

        return {
            "filename": document.filename,
            "url":
f"http://localhost:8000/{document.file_path}#page={page_no}"
        }

    finally:
        db.close()

# ==========================
# DELETE DOCUMENT
# ==========================
@router.delete("/documents/{document_id}")
def delete_document(document_id: int):

    db = SessionLocal()

    try:

        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if not document:

            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )

        filename = document.filename
        file_path = document.file_path

        ###################################################
        # Delete text embeddings
        ###################################################

        results = text_collection.get()

        ids = []

        for i, metadata in enumerate(results["metadatas"]):

            if metadata.get("source_file") == filename:

                ids.append(results["ids"][i])

        if ids:

            text_collection.delete(ids=ids)

        ###################################################
        # Delete image embeddings
        ###################################################

        try:

            results = image_collection.get()

            ids = []

            for i, metadata in enumerate(results["metadatas"]):

                if metadata.get("source_file") == filename:

                    ids.append(results["ids"][i])

            if ids:

                image_collection.delete(ids=ids)

        except Exception:

            pass

        ###################################################
        # Delete image metadata
        ###################################################

        db.query(DocumentImage).filter(

            DocumentImage.document_id == document_id

        ).delete()

        ###################################################
        # Delete chunks
        ###################################################

        db.query(Chunk).filter(

            Chunk.document_id == document_id

        ).delete()

        ###################################################
        # Delete document row
        ###################################################

        db.delete(document)

        db.commit()
        document_cache.remove_document(document.filename)

        ###################################################
        # Delete uploaded PDF
        ###################################################

        if file_path and os.path.exists(file_path):

            os.remove(file_path)

        ###################################################
        # Delete extracted images
        ###################################################

        image_folder = f"uploads/images/{document_id}"

        if os.path.exists(image_folder):

            shutil.rmtree(image_folder)

        return {

            "message": "Document deleted successfully"

        }

    finally:

        db.close()