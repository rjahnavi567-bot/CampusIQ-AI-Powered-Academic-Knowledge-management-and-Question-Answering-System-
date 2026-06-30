from app.services.chroma_service import (
    text_collection,
    image_collection
)
from app.services.embedding_service import create_embedding
from app.services.image_embedding_service import (
    embed_text_for_image_search
)


def hybrid_retrieve(
    question,
    page_no=None,
    source_file=None,
    top_k=10
):
    query_embedding = create_embedding(question)
    clip_embedding = embed_text_for_image_search(question)
    filters = []

    if page_no is not None:
        filters.append({"page_no": page_no})

    if source_file is not None:
        filters.append({"source_file": source_file})

    where = None

    if len(filters) == 1:
        where = filters[0]

    elif len(filters) > 1:
        where = {
        "$and": filters
    }

    # ---------------------------------
    # TEXT SEARCH (384-dimensional)
    # ---------------------------------

    query_args = {
    "query_embeddings": [query_embedding],
    "n_results": top_k
}

    if where is not None:
        query_args["where"] = where

    text_results = text_collection.query(**query_args)

    # ---------------------------------
    # IMAGE SEARCH (512-dimensional CLIP)
    # ---------------------------------

    if where:

        image_results = image_collection.query(
            query_embeddings=[clip_embedding],
            where=where,
            n_results=top_k
        )

    else:

        image_results = image_collection.query(
            query_embeddings=[clip_embedding],
            n_results=top_k
        )

    documents = []
    metadatas = []
    scores = []

    # ---------- Text ----------
    if len(text_results["documents"]) > 0:

        for doc, meta, score in zip(

            text_results["documents"][0],
            text_results["metadatas"][0],
            text_results["distances"][0]

        ):

            documents.append(doc)
            metadatas.append(meta)
            scores.append(score)

    # ---------- Images ----------
    if len(image_results["documents"]) > 0:

        for doc, meta, score in zip(

            image_results["documents"][0],
            image_results["metadatas"][0],
            image_results["distances"][0]

        ):

            documents.append(doc)
            metadatas.append(meta)
            scores.append(score)

    return documents, metadatas, scores