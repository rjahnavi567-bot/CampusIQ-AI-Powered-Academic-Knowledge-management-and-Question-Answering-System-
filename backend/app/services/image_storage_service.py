from app.database.models import DocumentImage
from app.services.chroma_service import image_collection
import os

from app.database.models import DocumentImage
from app.services.chroma_service import image_collection


def save_images(db, document_id, images):
    """
    Save image metadata into MySQL.
    """

    print("\nSaving image metadata...")

    for image in images:

        print("Saving:", image.path)

        record = DocumentImage(

            document_id=document_id,

            image_path=image.path,

            page_no=image.page_no,

            caption=image.caption,

            title=image.title,

            image_hash=image.image_hash,

            source_file=image.source_file,

            category=image.category,

            classification_confidence=image.classification_confidence,

            confidence_score=image.confidence_score

        )

        db.add(record)

    db.commit()

    print(f"Images saved: {len(images)}")
def store_images(images, document_id):
    """
    Store image embeddings into ChromaDB.
    """

    if not images:

        print("No images to store.")

        return

    ids = []

    documents = []

    embeddings = []

    metadatas = []

    for index, image in enumerate(images):

        if not image.clip_embedding:

            continue

        ids.append(

    f"image_{document_id}_page_{image.page_no}_{index}"

)

        documents.append(

f"""
IMAGE_HASH:
{image.image_hash}

TITLE:
{image.title}

CAPTION:
{image.caption}

OCR:
{image.ocr_text}

VISION:
{image.vision}

PAGE CONTEXT:
{image.page_context}
"""
        )

        embeddings.append(

            image.clip_embedding

        )

        metadatas.append(

            {

                "document_id": document_id,

                "type": "image",

                "page_no": image.page_no,

                "image_path": image.path,

                "caption": image.caption,

                "title": image.title,

                "category": image.category,

                "classification_confidence": float(
                    image.classification_confidence
                ),

                "confidence_score": float(
                    image.confidence_score
                ),

                "image_hash": image.image_hash,

                "source_file": image.source_file,

                "file_type": image.file_type

            }

        )

    image_collection.add(

        ids=ids,

        documents=documents,

        embeddings=embeddings,

        metadatas=metadatas

    )

    print(f"Stored {len(ids)} images.")