from app.services.chroma_service import (
    text_collection,
    image_collection
)

from app.services.image_embedding_service import (
    embed_text_for_image_search
)


def hybrid_retrieve(
    question,
    page_no=None,
    source_file=None,
    top_k=10
):

    where = {}

    if page_no is not None:
        where["page_no"] = page_no

    if source_file is not None:
        where["source_file"] = source_file

    # ---------------------------------
    # TEXT SEARCH (384-dimensional)
    # ---------------------------------

    if where:

        text_results = text_collection.query(
            query_texts=[question],
            where=where,
            n_results=top_k
        )

    else:

        text_results = text_collection.query(
            query_texts=[question],
            n_results=top_k
        )

    # ---------------------------------
    # IMAGE SEARCH (512-dimensional CLIP)
    # ---------------------------------

    clip_embedding = embed_text_for_image_search(question)

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