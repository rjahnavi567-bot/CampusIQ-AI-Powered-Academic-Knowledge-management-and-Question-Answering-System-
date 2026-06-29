from app.services.chroma_service import (
    text_collection,
    image_collection
)


def retrieve(
    question,
    page_no=None,
    source_file=None
):

    where = {}

    if page_no is not None:
        where["page_no"] = page_no

    if source_file is not None:
        where["source_file"] = source_file

    # ----------------------------
    # TEXT SEARCH
    # ----------------------------

    if where:

        text_results = text_collection.query(
            query_texts=[question],
            where=where,
            n_results=15
        )

    else:

        text_results = text_collection.query(
            query_texts=[question],
            n_results=15
        )

    # ----------------------------
    # IMAGE SEARCH
    # ----------------------------

    if where:

        image_results = image_collection.query(
            query_texts=[question],
            where=where,
            n_results=8
        )

    else:

        image_results = image_collection.query(
            query_texts=[question],
            n_results=8
        )

    documents = (
        text_results["documents"][0]
        + image_results["documents"][0]
    )

    metadatas = (
        text_results["metadatas"][0]
        + image_results["metadatas"][0]
    )

    scores = (
        text_results["distances"][0]
        + image_results["distances"][0]
    )

    return documents, metadatas, scores