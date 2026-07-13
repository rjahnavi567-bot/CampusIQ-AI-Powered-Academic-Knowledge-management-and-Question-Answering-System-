from .query_cleaner import clean_query
from .query_embedding import embed_query
from .chroma_retriever import retrieve


def retrieve_images(query):

    print("\n==============================")
    print("STAGE 11 : IMAGE RETRIEVAL")
    print("==============================")

    cleaned = clean_query(query)

    embedding = embed_query(cleaned)

    results = retrieve(embedding)

    print("Query :", cleaned)

    print()

    ids = results["ids"][0]
    distances = results["distances"][0]
    documents = results["documents"][0]

    for i in range(min(5, len(ids))):

        print(f"Rank {i+1}")

        print(ids[i])

        print(f"Distance : {distances[i]:.3f}")

        print(documents[i][:200])

        print()

    return results