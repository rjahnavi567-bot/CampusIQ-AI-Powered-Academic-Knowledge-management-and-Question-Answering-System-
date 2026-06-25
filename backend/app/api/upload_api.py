from fastapi import APIRouter, UploadFile, File
from app.services.document_processor import extract_text
from app.services.chunk_service import create_semantic_chunks
from app.services.chunk_storage_service import save_chunks
from app.services.chroma_service import collection
from app.database.models import Document
from app.database.connection import SessionLocal
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Annotated
from app.services.hash_service import (
    generate_file_hash
)
from app.services.signature_service import (
    create_content_signature
)
from app.services.title_service import (
    generate_title
)
from app.services.metadata_service import (
    extract_metadata
)
import json

from app.services.embedding_service1 import (
    create_embedding
)

from app.services.similarity_service1 import (
    cosine_similarity
)
from app.services.image_extraction_service import *
from app.services.image_extraction_service import (
    extract_images
)
from app.services.image_understanding_service import (
    understand_image
)
import shutil

import os
import shutil
import time
import hashlib
def clean_text(text):

    if not text:
        return ""

    return (
        str(text)
        .replace("\x00", "")
        .replace("\u0000", "")
    )
router = APIRouter()
ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".pptx",
    ".txt",
    ".jpg",
    ".jpeg",
    ".png"
}

MAX_FILE_SIZE = 50 * 1024 * 1024
def validate_file(file: UploadFile):

    extension = os.path.splitext(
        file.filename
    )[1].lower()

    if extension not in ALLOWED_EXTENSIONS:

        return {
            "valid": False,
            "message":
            f"Unsupported file type: {extension}"
        }

    file.file.seek(0, 2)

    file_size = file.file.tell()

    file.file.seek(0)

    if file_size > MAX_FILE_SIZE:

        return {
            "valid": False,
            "message":
            "File size exceeds 50 MB limit"
        }

    return {
        "valid": True
    }

# ==========================
# SINGLE FILE UPLOAD
# ==========================
@router.post("/upload")
def upload_file(file: UploadFile = File(...)):

    start_time = time.time()

    print(f"Starting upload: {file.filename}")

    validation = validate_file(file)

    if not validation["valid"]:

        raise HTTPException(
            status_code=400,
            detail=validation["message"]
        )

    db = SessionLocal()

    try:

        os.makedirs(
            "uploads",
            exist_ok=True
        )

        file_path = (
            f"uploads/{file.filename}"
        )

        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )
        file_hash = generate_file_hash(
    file_path
)
        print("FILE HASH:", file_hash)
        existing_document = (

    db.query(Document)

    .filter(
        Document.file_hash == file_hash
    )

    .first()

)

        if existing_document:

            os.remove(file_path)

            return {

        "error":
        "Duplicate document detected. Same content already exists.",
         "existing_document":
        existing_document.filename,

        "document_id":
        existing_document.id,

          "view_url":
    f"/documents/{existing_document.id}/view"

    }
            
        new_doc = Document(

    filename=file.filename,

    file_path=file_path,

    subject="General",

    unit="Unit-1",

    uploaded_by=1,

    status="Processing",

    chunk_count=0,

    file_hash=file_hash,

    content_signature="",
    embedding=""
)

        db.add(new_doc)
        db.commit()
        db.refresh(new_doc)

        document_id = new_doc.id

        pages = extract_text(file_path)
        images = []

        extension = (
    os.path.splitext(
        file_path
    )[1].lower()
)

        

        if extension == ".pdf":

            images = extract_pdf_images(
        file_path,
        document_id
    )

        elif extension == ".docx":

            images = extract_docx_images(
        file_path,
        document_id
    )

        elif extension == ".pptx":

            images = extract_pptx_images(
        file_path,
        document_id
    )

        elif extension in [
    ".png",
    ".jpg",
    ".jpeg"
]:

            images = extract_image_file(
        file_path
    )
            from app.services.image_caption_service import (
    generate_caption
)

            from app.services.ocr_service import (
    extract_ocr_text
)

            for image in images:

                image["caption"] = (
        generate_caption(
            image["path"]
        )
    )

                image["ocr_text"] = (
        extract_ocr_text(
            image["path"]
        )
    )

        metadata = extract_metadata(
    file_path
)

        suggested_title = generate_title(
    metadata
)
        if suggested_title == "Untitled_Document":

            full_text = ""

            for page in pages:

                full_text += (
            page["text"][:1000]
            + " "
        )

            words = []

            for word in full_text.split():

                if len(word) > 3:

                    words.append(word)

                if len(words) >= 8:

                    break

            if words:

                suggested_title = "_".join(words)

            else:

                suggested_title = os.path.splitext(
            file.filename
        )[0]
        suggested_title = (
    suggested_title
    .replace(":", "")
    .replace(",", "")
    .replace(".", "")
    .replace("/", "_")
    .replace("\\", "_")
    .replace("?", "")
    .replace("*", "")
    .replace('"', "")
    .replace("<", "")
    .replace(">", "")
    .replace("|", "")
)

        suggested_title = suggested_title[:100]
        extension = os.path.splitext(
    file.filename
)[1]

        new_filename = (
    suggested_title +
    extension
)

        counter = 1

        while os.path.exists(
    f"uploads/{new_filename}"
):

            new_filename = (
        f"{suggested_title}"
        f"_v{counter}"
        f"{extension}"
    )

            counter += 1

        new_file_path = (
    f"uploads/{new_filename}"
)

        os.rename(
    file_path,
    new_file_path
)

        file_path = new_file_path
        new_doc.filename = (
    new_filename
)

        new_doc.file_path = (
    file_path
)

        db.commit()
        

        content_signature = ""

        for page in pages:

            page_text = (
        page["text"]
        .replace("\x00", "")
        .replace("\u0000", "")
    )

            content_signature += (
        page_text[:1000] + "\n"
    )
        content_signature = (
    content_signature
    .replace("\x00", "")
    .replace("\u0000", "")
)
        embedding = create_embedding(
    content_signature[:4000]
)

        existing_docs = (
    db.query(Document)
    .filter(
        Document.embedding != None
    )
    .all()
)

        highest_similarity = 0

        similar_document = None

        for doc in existing_docs:

            try:

                old_embedding = json.loads(
            doc.embedding
        )

                similarity = cosine_similarity(
            embedding,
            old_embedding
        )

                if similarity > highest_similarity:

                    highest_similarity = similarity

                    similar_document = doc

            except:
                pass
        if highest_similarity > 0.95:
            db.delete(new_doc)
            db.commit()

            os.remove(file_path)
            return {

        "error":
        "Similar document already exists",

        "similarity":
        round(
            highest_similarity * 100,
            2
        ),

        "existing_document":
        similar_document.filename,

        "document_id":
        similar_document.id,

         "view_url":
    f"/documents/{similar_document.id}/view"
    }
        similarity_warning = None

        if (
    highest_similarity >= 0.90
    and highest_similarity <= 0.95
    and similar_document
):

            similarity_warning = {

        "similarity":
        round(
            highest_similarity * 100,
            2
        ),

        "existing_document":
        similar_document.filename,

        "document_id":
        similar_document.id
    }
        new_doc.content_signature = (
    str(content_signature)
    .replace("\x00", "")
    .replace("\u0000", "")
)
        new_doc.embedding = json.dumps(
    embedding
)
        print(
    "Embedding stored:",
    len(embedding)
)
        db.commit()

        chunks = []

        for page in pages:

            text = (
    page["text"]
    .replace("\x00", "")
    .replace("\u0000", "")
    .strip()
)

            if not text:
                continue

            page_chunks = create_semantic_chunks(text)

            for chunk in page_chunks:
                chunk["page_no"] = page["page_no"]

            chunks.extend(page_chunks)

        file_type = os.path.splitext(new_filename)[1]

        for chunk in chunks:
            chunk["source_file"] = new_filename
            chunk["file_type"] = file_type

        save_chunks(document_id, chunks)

        new_doc.chunk_count = len(chunks)
        new_doc.status = "Processed"

        db.commit()

        # Save to Chroma
        for i, chunk in enumerate(chunks):

            collection.add(
                ids=[f"{new_filename}_{i}"],
                documents=[chunk["content"]],
                metadatas=[
{
    "document_id":
    document_id,
                        "topic": chunk["topic"],
                        "keywords": ",".join(
                            chunk.get("keywords", [])
                        ),
                        "source_file": new_filename,
                        "file_type": file_type,
                        "page_no": chunk.get(
                            "page_no",
                            1
                        ),
                        "similarity_score": chunk.get(
                            "similarity_score",
                            0
                        )
                    }
                ]
            )
        # ==========================
# IMAGE EXTRACTION
# ==========================

        images = extract_images(
    file_path,
    document_id
)
        for image in images:

            understanding = understand_image(
        image["path"]
    )

            image["caption"] = (
        understanding["caption"]
    )

            image["ocr_text"] = (
        understanding["ocr_text"]
    )
            
        # ==========================
# STORE IMAGE DATA IN CHROMA
# ==========================

        print("\n===== IMAGE UNDERSTANDING =====")

        for image in images:

            print(
        "\nImage:",
        image["path"]
    )

            print(
        "Caption:",
        image["caption"]
    )

            print(
        "OCR:",
        image["ocr_text"]
    )
        for image in images:

            collection.add(

        ids=[
            f"image_"
            f"{document_id}_"
            f"{os.path.basename(image['path'])}"
        ],

        documents=[

    "Image Caption: "
    + image["caption"]

    + "\n\nOCR Text: "

    + image["ocr_text"]
],

        metadatas=[

    {

        "document_id":
        document_id,

        "type":
        "image",

        "page_no":
        image["page_no"],

        "image_path":
        image["path"],

        "caption":
        image["caption"]
    }
]
    )

        print(
    f"Extracted {len(images)} images"
)    
        print(
    f"Finished {file.filename} in "
    f"{round(time.time() - start_time, 2)} sec"
)
        response = {

    "message":
    "File processed successfully",

    "original_filename":
    file.filename,

    "stored_filename":
    new_filename,

    "suggested_title":
    suggested_title,

    "chunks_created":
    len(chunks),
    "images_extracted":
    len(images),
    "images_understood":
len(images),
}
        if similarity_warning:

            response["warning"] = (
        "Similar document exists"
    )

            response["similarity"] = (
        similarity_warning["similarity"]
    )

            response["existing_document"] = (
        similarity_warning["existing_document"]
    )

        return response
    finally:
        db.close()



