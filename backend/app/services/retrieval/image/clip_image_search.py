from app.config.qdrant import client

from app.services.image_embedding_service import (
    embed_text_for_image_search
)

COLLECTION_NAME = "image_vectors"


def retrieve_clip_images(
    question,
    source_file=None,
    page_no=None,
    top_k=10
):
    """
    Search image vectors stored in Qdrant using CLIP text embeddings.
    """

    print("\n==============================")
    print("STAGE 11.1 : CLIP IMAGE SEARCH")
    print("==============================")

    # ---------------------------------
    # Generate CLIP text embedding
    # ---------------------------------

    query_embedding = embed_text_for_image_search(question)

    print(f"Embedding Dimension : {len(query_embedding)}")

    # ---------------------------------
    # Build Qdrant Filter
    # ---------------------------------

    must_conditions = []

    if source_file is not None:

        must_conditions.append({

            "key": "source_file",

            "match": {

                "value": source_file

            }

        })

    if page_no is not None:

        must_conditions.append({

            "key": "page_no",

            "match": {

                "value": page_no

            }

        })

    query_filter = None

    if len(must_conditions) > 0:

        query_filter = {

            "must": must_conditions

        }

    # ---------------------------------
    # Search Qdrant
    # ---------------------------------

    try:

        results = client.search(

            collection_name=COLLECTION_NAME,

            query_vector=query_embedding,

            limit=top_k,

            query_filter=query_filter

        )

    except Exception as e:

        print("\nQDRANT SEARCH FAILED")

        print(e)

        return []

    # ---------------------------------
    # Build Results
    # ---------------------------------

    retrieved = []

    for hit in results:

        payload = hit.payload

        retrieved.append({

            "document": payload.get(

                "search_text",

                ""

            ),

            "metadata": {

                "document_id": payload.get(

                    "document_id"

                ),

                "page_no": payload.get(

                    "page_no"

                ),

                "image_path": payload.get(

                    "path"

                ),

                "caption": payload.get(

                    "caption"

                ),

                "title": payload.get(

                    "title"

                ),

                "category": payload.get(

                    "category"

                ),

                "source_file": payload.get(

                    "source_file"

                ),

                "retrieval_type": "clip_image"

            },

            "score": hit.score

        })

    print(f"Retrieved Images : {len(retrieved)}")

    if len(retrieved) > 0:

        print("\nTop Results\n")

        for item in retrieved[:5]:

            print(

                f'Page {item["metadata"]["page_no"]} | '

                f'{item["score"]:.3f} | '

                f'{item["metadata"]["category"]}'

            )

    return retrieved