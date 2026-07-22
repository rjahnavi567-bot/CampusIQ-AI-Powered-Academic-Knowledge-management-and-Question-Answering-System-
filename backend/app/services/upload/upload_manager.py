import os
import json
import shutil
import time
import traceback
import fitz
from app.services.statistics.timer import Timer
from fastapi import HTTPException
from app.database.connection import SessionLocal
from app.database.models import Document
from concurrent.futures import ThreadPoolExecutor
from app.services.document_processor import extract_text
from app.services.chunk_storage_service import save_chunks
from app.services.text_storage_service import store_text_chunks
from app.services.image_storage_service import (
    save_images,
    store_images
)
from app.services.hash_service import generate_file_hash

from app.services.upload.file_validation import validate_file
from app.services.upload.document_initializer import (
    create_document,
    finalize_document,
    update_document_filename
)

from app.services.upload.duplicate_detector import (
    check_similarity
)

from app.services.upload.title_generator import (
    generate_document_title
)

from app.services.upload.text_pipeline import (
    process_text_pages
)
from app.services.upload.response_builder import (
    build_upload_response
)
from app.services.image_v2.image_pipeline_v2 import process_images_v2
from app.services.image_storage_service import (
    save_images,
    store_images as store_text_embeddings
)

from app.services.image_v2.image_vector_store import (
    store_images as store_clip_embeddings
)
from app.services.statistics import (
    stats,
    upload_stats
)
from app.database.models import Chunk, DocumentImage
from app.services.chroma_service import (
    text_collection,
    image_collection
)
from app.services.statistics.statistics_collector import collector
def cleanup_upload(db, document_id, filename, file_path):
    import shutil
    import os

    print("\nRunning upload rollback...")

    # -------------------------
    # Delete SQL records
    # -------------------------

    """"db.query(Chunk).filter(
        Chunk.document_id == document_id
    ).delete()

    db.query(DocumentImage).filter(
        DocumentImage.document_id == document_id
    ).delete()

    db.query(Document).filter(
        Document.id == document_id
    ).delete()

    db.commit()"""

    # -------------------------
    # Delete Chroma Text
    # -------------------------

    try:

        results = text_collection.get()

        ids = []

        for i, meta in enumerate(results["metadatas"]):

            if meta.get("source_file") == filename:

                ids.append(results["ids"][i])

        if ids:

            text_collection.delete(ids=ids)

            print(f"Deleted {len(ids)} text embeddings")

    except Exception as e:

        print("Text cleanup failed:", e)

    # -------------------------
    # Delete Chroma Images
    # -------------------------

    try:

        results = image_collection.get()

        ids = []

        for i, meta in enumerate(results["metadatas"]):

            if meta.get("document_id") == document_id:

                ids.append(results["ids"][i])

        if ids:

            image_collection.delete(ids=ids)

            print(f"Deleted {len(ids)} image embeddings")

    except Exception as e:

        print("Image cleanup failed:", e)

    # -------------------------
    # Delete uploaded pdf
    # -------------------------

    if os.path.exists(file_path):

        os.remove(file_path)

    # -------------------------
    # Delete extracted images
    # -------------------------

    image_folder = f"uploads/images/{document_id}"

    if os.path.exists(image_folder):

        shutil.rmtree(image_folder)

    print("Rollback completed.")
class UploadManager:
    def upload(self, file):
        upload_stats.reset()
        start_time = time.time()
        processing_timer = Timer()
        processing_timer.start()


        start_time = time.time()

        print(f"\nStarting Upload : {file.filename}")

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

            file_path = f"uploads/{file.filename}"

            with open(file_path, "wb") as buffer:

                shutil.copyfileobj(
                    file.file,
                    buffer
                )

            # ------------------------------------
            # Generate Hash
            # ------------------------------------

            file_hash = generate_file_hash(
                file_path
            )

            print("File Hash :", file_hash)

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
                    "Duplicate document detected.",

                    "existing_document":
                    existing_document.filename,

                    "document_id":
                    existing_document.id,

                    "view_url":
                    f"/documents/{existing_document.id}/view"

                }

            # ------------------------------------
            # Create Database Record
            # ------------------------------------

            new_doc = create_document(

                db=db,

                filename=file.filename,

                file_path=file_path,

                file_hash=file_hash

            )

            document_id = new_doc.id

            print(
                f"Document ID : {document_id}"
            )

            # ------------------------------------
            # Extract Text
            # ------------------------------------

            pages = extract_text(
                file_path
            )
            page_lookup = {}

            for page in pages:

                page_lookup[page["page_no"]] = page["text"]
            page_text_lookup = {}

            for page in pages:

                page_no = page["page_no"]

                if page_no not in page_text_lookup:
                    page_text_lookup[page_no] = ""

                page_text_lookup[page_no] += "\n" + page["text"]

            # ------------------------------------
            # Generate Better Title
            # ------------------------------------

            print("Generating document title...")

            suggested_title, new_filename, new_file_path = (

                generate_document_title(

                    file_path=file_path,

                    pages=pages,

                    original_filename=file.filename

                )

            )
            try:
            # Rename the actual file
                os.rename(file_path, new_file_path)

                file_path = new_file_path
            
            except Exception:

                print("Rename failed.")

                new_filename = file.filename

                new_file_path = file_path

            update_document_filename(

    db=db,

    document=new_doc,

    new_filename=new_filename,

    new_path=new_file_path

)

            print("New Filename :", new_filename)
            upload_stats.increment("Total Documents Uploaded")

            extension = os.path.splitext(file_path)[1].lower()


            if extension == ".pdf":
                upload_stats.increment("Total PDF Files")

            elif extension == ".docx":
                upload_stats.increment("Total DOCX Files")

            elif extension == ".pptx":
                upload_stats.increment("Total PPTX Files")

            elif extension == ".txt":
                upload_stats.increment("Total TXT Files")

            elif extension in [".png", ".jpg", ".jpeg"]:
                upload_stats.increment("Total Image Files")

            # ------------------------------------
            # Process Images
            # ------------------------------------

            print("\nStarting Text & Image Pipelines...")
            ####################################################
# Build Page Lookup
####################################################



            pdf = fitz.open(file_path)

            page_lookup = {}

            for page_index, page in enumerate(pdf, start=1):

                page_lookup[page_index] = {

        "width": page.rect.width,
        "height": page.rect.height

    }

            pdf.close()

            print("\nPage Lookup Built")

            for page_no in list(page_lookup.keys())[:5]:

                print(

        f"Page {page_no} : "

        f"{page_lookup[page_no]['width']} x "

        f"{page_lookup[page_no]['height']}"

    )

            with ThreadPoolExecutor(max_workers=2) as executor:

                image_future = executor.submit(

    process_images_v2,

    file_path=file_path,

    document_id=document_id,

    page_lookup=page_lookup,

    page_text_lookup=page_text_lookup

)

                text_future = executor.submit(

        process_text_pages,

        pages=pages,

        filename=new_filename

    )

                images = image_future.result()

                chunks, content_signature = text_future.result()
                print("\n" + "=" * 70)
                print("IMAGE PIPELINE V2 OUTPUT")
                print("=" * 70)

                for i, img in enumerate(images, start=1):

                    print(f"\nImage {i}")

                    print(f"Page          : {img.page_no}")

                    print(f"Category      : {img.category}")

                    print(f"Caption       : {img.caption}")

                    print(f"OCR           : {img.ocr_text[:120]}")

                    print(f"Embedding Dim : {len(img.clip_embedding)}")

                    print(f"Path          : {img.path}")

                    print("\nTotal Images :", len(images))
            

            # ------------------------------------
            # Similarity Detection
            # ------------------------------------

            print("Checking document similarity...")

            embedding, highest_similarity, similar_document = (

                check_similarity(

                    db,

                    content_signature

                )

            )

            if highest_similarity > 0.95:

                db.delete(new_doc)

                db.commit()

                os.remove(file_path)

                return {

                    "error":

                    "Very similar document already exists.",

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

            # ------------------------------------
            # Save Signature + Embedding
            # ------------------------------------

            new_doc.content_signature = (

                str(content_signature)

                .replace("\x00", "")

                .replace("\u0000", "")

            )

            new_doc.embedding = json.dumps(

                embedding

            )

            

            print("Similarity Check Complete.")
            try:            
                # ------------------------------------
            # Save Chunks
            # ------------------------------------

                print("Saving chunks...")

                save_chunks(

                document_id,

                chunks

            )
                collector.increment(
    "Total Metadata Records Generated",
    len(chunks)
)
                collector.increment(
    "Total Chunks Stored",
    len(chunks)
)
            # ------------------------------------
            # Store Text Embeddings
            # ------------------------------------
                print("Uploading text embeddings to Chroma...")

                store_text_chunks(

                document_id,

                chunks

            )

                print("Saving image metadata...")

                save_images(db, document_id, images)
                collector.increment(
    "Total Images Stored",
    len(images)
)

                print("\nStoring text image embeddings...")

                store_text_embeddings(
    images,
    document_id
)
                collector.increment(
    "Total Embeddings Generated",
    len(chunks)
)

                print("\nStoring CLIP image embeddings...")

                store_clip_embeddings(
    images
)
                collector.increment(
    "Total Embeddings Generated",
    len(images)
)
                
            except Exception:

                cleanup_upload(
        db,
        document_id,
        new_filename,
        file_path
    )


                raise
            print(

                f"Stored {len(images)} images."

            )

            # ------------------------------------
            # Update Database
            # ------------------------------------

            finalize_document(

                db=db,

                document=new_doc,

                chunk_count=len(chunks)

            )
            db.commit()
            collector.increment(
    "Total Documents Stored"
)


            elapsed = round(

                time.time() - start_time,

                2

            )

            print(

                f"\nUpload Finished in {elapsed} seconds."

            )
            # ---------------------------------------
# Merge current upload into global stats
# ---------------------------------------

            stats.merge_upload_statistics(upload_stats)
            stats.increment("Total Successful Uploads")

            processing_time = processing_timer.stop()

            stats.add_time(
    "End-to-End Document Processing Time",
    processing_time
)
            print("\n========================================")
            print("CURRENT UPLOAD STATISTICS")
            print("========================================")

            report = upload_stats.report()

            for key, value in report.items():
                print(f"{key:<35}: {value}")

            print("========================================\n")
            print("\n========================================")
            print("GLOBAL STATISTICS")
            print("========================================")

            global_report = stats.report()

            for key, value in global_report.items():

                print(f"{key:<40}: {value}")

            print("========================================\n")



            # ------------------------------------
            # Build API Response
            # ------------------------------------

            return build_upload_response(

                original_filename=file.filename,

                stored_filename=new_filename,

                suggested_title=suggested_title,

                chunks=chunks,

                images=images,

                similarity_warning=similarity_warning

            )

        except Exception as e:

            stats.increment("Total Failed Uploads")

            db.rollback()

            try:

                cleanup_upload(
            db,
            document_id,
            new_filename,
            file_path
        )

            except Exception as cleanup_error:

                    print("Cleanup Error:", cleanup_error)

            print("\nUPLOAD FAILED")

            traceback.print_exc()

            raise HTTPException(
        status_code=500,
        detail=str(e)
    )

upload_manager = UploadManager()