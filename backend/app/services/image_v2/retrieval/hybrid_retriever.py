import re

from .chroma_retriever import retrieve


# ------------------------------
# tokenize
# ------------------------------

def tokenize(text):

    if text is None:
        return set()

    words = re.findall(r"[a-zA-Z0-9]+", text.lower())

    return set(words)


# ------------------------------
# keyword overlap
# ------------------------------

def overlap(query, text):

    q = tokenize(query)
    t = tokenize(text)

    if len(q) == 0:
        return 0

    return len(q & t) / len(q)


# ------------------------------
# rerank
# ------------------------------

def rerank(query, results):

    docs = results["documents"][0]
    metas = results["metadatas"][0]
    ids = results["ids"][0]
    distances = results["distances"][0]

    ranked = []

    for idx in range(len(docs)):

        doc = docs[idx]

        semantic = 1 - distances[idx]

        keyword_score = overlap(query, doc)

        hybrid = (

            semantic * 0.70 +

            keyword_score * 0.30

        )

        ranked.append({

            "id": ids[idx],

            "score": hybrid,

            "semantic": semantic,

            "keyword": keyword_score,

            "document": doc,

            "metadata": metas[idx]

        })

    ranked.sort(

        key=lambda x: x["score"],

        reverse=True

    )

    return ranked


# ------------------------------
# search
# ------------------------------

def hybrid_search(

    query,

    embedding,

    top_k=20

):

    results = retrieve(

        embedding,

        top_k=top_k

    )

    return rerank(

        query,

        results

    )