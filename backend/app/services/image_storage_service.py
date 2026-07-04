from app.database.models import DocumentImage
from app.services.chroma_service import image_collection
from app.services.image_embedding_service import embed_image
import os


def save_images(db, document_id, images):
    """
    Save image metadata into MySQL.
    """

    for image in images:

        record = DocumentImage(

    document_id=document_id,

    image_path=image["path"],

    page_no=image["page_no"],

    caption=image.get("caption", ""),

    title=image.get("title", ""),

    image_hash=image.get("image_hash", ""),

    source_file=image.get("source_file", "")

)
        category=image.get("category", ""),

        classification_confidence=image.get(
    "classification_confidence",
    0.5
),

        db.add(record)
    print("\nSaving image metadata...")

    for image in images:
        print(image["path"])

    db.commit()
    print("Images saved:", len(images))

def store_images(images, document_id):
    """
    Store all image embeddings into ChromaDB
    using a bulk insert.
    """

    if not images:
        print("No images to store.")
        return

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for image in images:

        if image.get("clip_embedding") is None:
            continue

        ids.append(
            f"image_{document_id}_{image['image_hash']}"
        )

        documents.append(
f"""
IMAGE_HASH:
{image.get("image_hash","")}

TITLE:
{image.get("title","")}

CAPTION:
{image.get("caption","")}

OCR:
{image.get("ocr_text","")}

VISION:
{image.get("vision","")}

PAGE CONTEXT:
{image.get("page_text","")}
"""
        )

        embeddings.append(
            image["clip_embedding"]
        )

        metadatas.append(
            {
                "document_id": document_id,
                "type": "image",
                "page_no": image["page_no"],
                "image_path": image["path"],
                "caption": image.get("caption", ""),
                "title": image.get("title", ""),
                "category": image.get("category", ""),

"classification_confidence": float(

    image.get(

        "classification_confidence",

        0.5

    )

),
                "image_hash": image.get("image_hash", ""),
                "source_file": image.get("source_file", ""),
                "file_type": image.get("file_type", "")
            }
        )

    image_collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(
        f"Stored {len(ids)} images."
    )