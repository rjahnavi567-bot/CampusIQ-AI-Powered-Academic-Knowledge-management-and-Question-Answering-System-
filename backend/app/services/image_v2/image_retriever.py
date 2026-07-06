from qdrant_client import QdrantClient

from qdrant_client.models import Filter
from app.config.qdrant import client
from app.services.image_v2.clip_service import embed_text


client = QdrantClient(
    host="localhost",
    port=6333
)

COLLECTION = "image_vectors"


def search_images(query, limit=5):

    vector = embed_text(query)

    results = client.query_points(

        collection_name=COLLECTION,

        query=vector,

        limit=limit

    )

    return results.points