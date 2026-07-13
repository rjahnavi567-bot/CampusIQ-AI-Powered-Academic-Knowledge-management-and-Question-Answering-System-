from .retrieval.hybrid_retriever import hybrid_search
from .retrieval.cross_encoder_reranker import rerank
from .context.context_pipeline import build_contexts
from .embedding_generator import get_embedding_model


def search_images(query):

    print("\n==========================")
    print("IMAGE SEARCH PIPELINE")
    print("==========================")

    model = get_embedding_model()

    query_embedding = model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    # Stage 11.1
    results = hybrid_search(
        query,
        query_embedding,
        top_k=30
    )

    # Stage 11.2
    results = rerank(
        query,
        results
    )

    # Stage 11.3
    results = build_contexts(results)

    return results