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

# ---------------------------------
# TEXT SEARCH
# ---------------------------------

    query_args = {
    "query_embeddings": [query_embedding],
    "n_results": top_k
}

    if where is not None:
        query_args["where"] = where

    print("\n===== CHROMA FILTER =====")
    print(where)
    print("=========================\n")

    text_results = text_collection.query(**query_args)

# ---------------------------------
# IMAGE SEARCH
# ---------------------------------

    try:
 
        image_args = {
        "query_embeddings": [clip_embedding],
        "n_results": top_k
    }

        if where is not None:
            image_args["where"] = where

        image_results = image_collection.query(**image_args)

    except Exception as e:

        print("\nIMAGE SEARCH FAILED")
        print(e)

        image_results = {
        "documents":[[]],
        "metadatas":[[]],
        "distances":[]
    }

    documents=[]
    metadatas=[]
    scores=[]

# ---------------- TEXT ----------------

    if text_results["documents"]:
        for doc,meta,score in zip(
        text_results["documents"][0],
        text_results["metadatas"][0],
        text_results["distances"][0]
    ):

            meta["retrieval_type"]="text"

        documents.append(doc)
        metadatas.append(meta)
        scores.append(score)

# ---------------- IMAGE ----------------

    if image_results["documents"]:
        for doc,meta,score in zip(
        image_results["documents"][0],
        image_results["metadatas"][0],
        image_results["distances"][0]
    ):
            meta["retrieval_type"]="image"

        documents.append(doc)
        metadatas.append(meta)
        scores.append(score)

    print("\nRetrieved Text :",len(text_results["documents"][0]))
    print("Retrieved Images :",len(image_results["documents"][0]))
    print("Total :",len(documents))

    return documents,metadatas,scores