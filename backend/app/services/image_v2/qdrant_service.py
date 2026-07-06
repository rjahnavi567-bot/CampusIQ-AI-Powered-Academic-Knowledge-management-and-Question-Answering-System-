from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import uuid
client = QdrantClient(
    host="localhost",
    port=6333
)

COLLECTION = "image_vectors"


def upload_images(images):

    points = []

    for idx, image in enumerate(images):

        payload = {

            "page_no": image.page_no,

            "path": image.path,

            "caption": image.caption,

            "ocr_text": image.ocr_text,

            "classification": image.category,

            "page_context": image.page_context,

            "search_text": image.search_text,

            "document_id": image.document_id,

            "source": image.source

        }

        point = PointStruct(

            id=str(uuid.uuid4()),

            vector=image.clip_embedding,

            payload=payload

        )

        points.append(point)

    client.upsert(

        collection_name=COLLECTION,

        points=points

    )

    print(f"Uploaded {len(points)} images.")