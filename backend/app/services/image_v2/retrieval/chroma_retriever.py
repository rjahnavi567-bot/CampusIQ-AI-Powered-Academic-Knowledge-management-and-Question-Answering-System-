from ..vector_storage import collection


def retrieve(query_embedding, top_k=20):

    results = collection.query(

        query_embeddings=[query_embedding],

        n_results=top_k

    )

    return results