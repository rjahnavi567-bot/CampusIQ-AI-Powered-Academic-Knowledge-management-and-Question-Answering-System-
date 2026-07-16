def compute_positive_score(det):

    score = 0

    reasons = []

    if det.get("is_photo", False):

        score += 3

        reasons.append("Photo")

    return {

        "positive_score": score,

        "positive_reason": reasons

    }