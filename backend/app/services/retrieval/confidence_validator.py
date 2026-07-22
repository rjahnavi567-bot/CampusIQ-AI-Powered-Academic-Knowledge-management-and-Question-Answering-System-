CONFIDENCE_THRESHOLD = 0.60


def validate_retrieval(ranked_results):
    """
    Returns:
        (is_confident, top_score)
    """

    if not ranked_results:
        return False, 0.0

    top_score = ranked_results[0]["score"]

    if top_score >= CONFIDENCE_THRESHOLD:
        return True, top_score

    return False, top_score