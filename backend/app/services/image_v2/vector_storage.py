import chromadb
import os

# ---------------------------------------------
# Chroma Collection
# ---------------------------------------------

client = chromadb.PersistentClient(
    path="./chroma_db"
)
try:
    client.delete_collection("academic_images")
except:
    pass

collection = client.get_or_create_collection(
    name="academic_images"
)


# ---------------------------------------------
# Store One Image
# ---------------------------------------------

def store_image(image):

    if not image.embedding_valid:
        return

    image_id = (
    f"{image.document_id}_"
    f"{image.page_no}_"
    f"{os.path.basename(image.path)}"
)
    image.vector_id = image_id

    metadata = {

        "document_id": image.document_id,
        "page": image.page_no,
        "decision": image.final_decision,
        "layout": image.layout_type,
        "orientation": image.orientation,
        "resolution": image.normalized_metadata["resolution"],
        "metadata_score": image.metadata_score,
        "quality_score": image.quality_score,
        "ocr_score": image.ocr_score,
        "layout_score": image.layout_score,
        "vision_score": image.vision_score

    }

    collection.add(

        ids=[image_id],

        embeddings=[image.embedding],

        documents=[image.search_text],

        metadatas=[metadata]

    )


# ---------------------------------------------
# Store All Images
# ---------------------------------------------

def store_vectors(images):

    print("\n==============================")
    print("STAGE 10.3 : VECTOR STORAGE")
    print("==============================")

    stored = 0

    for image in images:

        if image.embedding_valid:

            store_image(image)

            stored += 1

    print(f"Vectors Stored : {stored}")

    return images