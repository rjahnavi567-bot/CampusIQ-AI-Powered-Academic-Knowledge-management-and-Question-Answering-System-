from app.services.retrieval.hybrid_retrieval_service import hybrid_retrieve
from app.services.retrieval.unified.score_normalizer import normalize_results


def search_images(
    query,
    page_no=None,
    source_file=None,
    top_k=10
):

    print("\n==========================")
    print("IMAGE SEARCH PIPELINE")
    print("==========================")

    ####################################################
    # Stage 12.1 : Hybrid Retrieval
    ####################################################

    documents, metadatas, scores = hybrid_retrieve(

        question=query,

        page_no=page_no,

        source_file=source_file,

        top_k=top_k

    )

    ####################################################
    # Stage 12.2 : Score Normalization
    ####################################################

    results = normalize_results(

        documents,

        metadatas,

        scores

    )

    return results