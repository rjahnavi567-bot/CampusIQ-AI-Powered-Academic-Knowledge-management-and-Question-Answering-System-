from app.services.chroma_service import (
    text_collection,
    image_collection
)
from app.services.embedding_service import create_embedding
from app.services.image_embedding_service import (
    embed_text_for_image_search
)
from app.services.retrieval.unified.score_normalizer import normalize_scores
def hybrid_retrieve(
    question,
    page_no=None,
    source_file=None,
    top_k=10
):
    query_embedding = create_embedding(question)
    clip_embedding = embed_text_for_image_search(question)

    print("\n===== QUERY EMBEDDING =====")
    print("Query embedding length:", len(clip_embedding))
    print("===========================\n")

    filters = []

    if page_no is not None:
        filters.append({"page_no": page_no})

    if source_file is not None:
        filters.append({"source_file": source_file})

    where = None

    if len(filters) == 1:
        where = filters[0]

    elif len(filters) > 1:
        where = {"$and": filters}

    # --------------------------
    # TEXT SEARCH
    # --------------------------

    text_args = {
        "query_embeddings": [query_embedding],
        "n_results": top_k
    }

    if where:
        text_args["where"] = where

    try:

        text_results = text_collection.query(**text_args)

    except Exception as e:

        print("TEXT SEARCH FAILED")
        print(e)

        text_results = {
            "documents":[[]],
            "metadatas":[[]],
            "distances":[[]]
        }

    # --------------------------
    # IMAGE SEARCH
    # --------------------------

    image_args = {
        "query_embeddings":[clip_embedding],
        "n_results":top_k
    }

    if where:
        image_args["where"] = where

    try:

        image_results = image_collection.query(**image_args)

    except Exception as e:

        print("IMAGE SEARCH FAILED")
        print(e)

        image_results = {
            "documents":[[]],
            "metadatas":[[]],
            "distances":[[]]
        }

    documents = []
    metadatas = []
    scores = []

    # --------------------------
    # TEXT RESULTS
    # --------------------------

    if (
        text_results.get("documents")
        and len(text_results["documents"][0]) > 0
    ):

        for doc, meta, score in zip(

            text_results["documents"][0],
            text_results["metadatas"][0],
            text_results["distances"][0]

        ):

            meta["retrieval_type"] = "text"

            documents.append(doc)
            metadatas.append(meta)
            scores.append(score)

    # --------------------------
    # IMAGE RESULTS
    # --------------------------

    if (
        image_results.get("documents")
        and len(image_results["documents"][0]) > 0
    ):

        for doc, meta, score in zip(

            image_results["documents"][0],
            image_results["metadatas"][0],
            image_results["distances"][0]

        ):

            meta["retrieval_type"] = "image"

            documents.append(doc)
            metadatas.append(meta)
            scores.append(score)

    # --------------------------
    # Stage 12.2
    # Score Normalization
    # --------------------------

    scores = normalize_scores(scores)

    print("\n===== RETRIEVAL SUMMARY =====")
    print("Text Results :", sum(
        1 for m in metadatas
        if m["retrieval_type"] == "text"
    ))
    print("Image Results:", sum(
        1 for m in metadatas
        if m["retrieval_type"] == "image"
    ))
    print("Total Results :", len(documents))
    print("=============================\n")

    return documents, metadatas, scores

# ==========================================================
# TEXT RETRIEVAL ONLY
# ==========================================================
def retrieve_text(
    question,
    page_no=None,
    source_file=None,
    top_k=8
):

    query_embedding = create_embedding(question)

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

    query_args = {
        "query_embeddings": [query_embedding],
        "n_results": top_k
    }

    if where:
        query_args["where"] = where

    try:

        query_results = text_collection.query(**query_args)

    except Exception as e:

        print("TEXT SEARCH FAILED")
        print(e)

        return [], [], []

    documents = []
    metadatas = []
    scores = []

    if (
        query_results.get("documents")
        and len(query_results["documents"][0]) > 0
    ):

        for doc, meta, score in zip(

            query_results["documents"][0],
            query_results["metadatas"][0],
            query_results["distances"][0]

        ):

            meta["retrieval_type"] = "text"

            documents.append(doc)
            metadatas.append(meta)
            scores.append(score)

    # ------------------------------
    # Stage 12.2
    # Normalize Scores
    # ------------------------------

    scores = normalize_scores(scores)

    return documents, metadatas, scores

# ==========================================================
# IMAGE RETRIEVAL ONLY
# ==========================================================

def retrieve_images(
    question,
    pages,
    source_file=None,
    top_k=6
):

    clip_embedding = embed_text_for_image_search(question)

    page_filters = []

    for page in pages:

        page_filters.append({
            "page_no": page
        })

    where = {
        "$or": page_filters
    }

    if source_file:

        where = {
            "$and": [
                {
                    "source_file": source_file
                },
                where
            ]
        }

    try:

        query_results = image_collection.query(

            query_embeddings=[clip_embedding],

            where=where,

            n_results=top_k,

            include=[
                "documents",
                "metadatas",
                "distances",
                "embeddings"
            ]

        )

    except Exception as e:

        print("IMAGE SEARCH FAILED")
        print(e)

        return [], [], []

    documents = []
    metadatas = []
    scores = []

    if (

        query_results.get("documents")

        and

        len(query_results["documents"][0]) > 0

    ):

        for doc, meta, score, embedding in zip(

            query_results["documents"][0],

            query_results["metadatas"][0],

            query_results["distances"][0],

            query_results["embeddings"][0]

        ):

            meta["retrieval_type"] = "image"

            meta["clip_embedding"] = embedding

            documents.append(doc)

            metadatas.append(meta)

            scores.append(score)

    # -----------------------------------
    # Stage 12.2
    # Normalize Scores
    # -----------------------------------

    scores = normalize_scores(scores)

    return documents, metadatas, scores