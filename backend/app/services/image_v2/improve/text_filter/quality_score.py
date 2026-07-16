"""
Combines all filtering signals into one quality score.

Instead of rejecting immediately,
every filter contributes to a score.

Higher score = more likely to be useless.
"""

REJECT_THRESHOLD = 5


def compute_quality_score(result):

    score = 0

    reasons = []

    # -----------------------------
    # OCR
    # -----------------------------

    if result["word_count"] > 120:

        score += 2

        reasons.append("High OCR")

    if result["char_count"] > 900:

        score += 1

        reasons.append("Many Characters")

    if result["text_ratio"] > 0.70:

        score += 1

        reasons.append("Dense Text")

    # -----------------------------
    # Connected Components
    # -----------------------------

    if result["components"] > 3500:

        score += 1

        reasons.append("Many Components")

    # -----------------------------
    # Edge Density
    # -----------------------------

    edge = result["edge_density"]

    if edge > 0.50:

        score += 1

        reasons.append("High Edge Density")

    elif edge < 0.01:

        score += 1

        reasons.append("Very Few Edges")

    # -----------------------------
    # White Ratio
    # -----------------------------

    if result["white_ratio"] > 0.97:

        score += 1

        reasons.append("Mostly White")

    # -----------------------------
    # Aspect Ratio
    # -----------------------------

    ratio = result["aspect_ratio"]

    if ratio > 12 or ratio < 0.12:

        score += 1

        reasons.append("Extreme Aspect Ratio")

    # -----------------------------
    # Final Decision
    # -----------------------------

    return {

        "score": score,

        "reject": score >= REJECT_THRESHOLD,

        "reasons": reasons

    }