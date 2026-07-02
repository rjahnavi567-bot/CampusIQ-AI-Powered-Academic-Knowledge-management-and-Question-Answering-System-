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
            caption=image["caption"]
        )

        db.add(record)
    print("\nSaving image metadata...")

    for image in images:
        print(image["path"])

    db.commit()
    print("Images saved:", len(images))


def store_images(images, document_id):
    """
    Store image captions + OCR into ChromaDB.
    """
    print("\nUploading image embeddings...")

    count = 0
    for image in images:
        count += 1

        print(
    "Uploading:",
    image["path"]
)
        

        embedding = embed_image(image["path"])

        image_collection.add(

    ids=[
        f"image_{document_id}_{os.path.basename(image['path'])}"
    ],

    embeddings=[
        image["clip_embedding"]
    ],

    documents=[
        image["caption"] + "\n\n" + image["ocr_text"]
    ],

    metadatas=[
        {
            "document_id": document_id,
            "type": "image",
            "page_no": image["page_no"],
            "image_path": image["path"],
            "caption": image.get("caption", ""),
            "source_file": image.get("source_file", "unknown")
        }
    ]
)