import re
def calculate_confidence(image):

    score = 0.0

    reasons = []

    title = image.get("title", "")

    if len(title) > 8:
        score += 0.20
        reasons.append("title")

    classifier_conf = image.get(
        "classification_confidence",
        0.5
    )

    score += classifier_conf * 0.30

    if classifier_conf >= 0.7:
        reasons.append("classifier")

    caption = image.get("caption", "")

    if len(caption.split()) >= 4:

        bad_words = [
            "page",
            "document",
            "text",
            "paragraph",
            "website",
            "logo",
            "icon"
        ]

        if not any(w in caption.lower() for w in bad_words):

            score += 0.15
            reasons.append("caption")

    ocr = image.get("ocr_text", "")

    words = len(ocr.split())

    if 2 <= words <= 60:
        score += 0.10
        reasons.append("ocr")

    context = image.get(
        "page_text",
        ""
    ).lower()

    if len(context) > 150:

        score += 0.05

        keywords = [
            "figure",
            "diagram",
            "architecture",
            "algorithm",
            "flow",
            "table",
            "graph"
        ]

        if any(k in context for k in keywords):
            score += 0.05
            reasons.append("context")

    vision = image.get("vision", "")

    if len(vision) > 80:
        score += 0.15
        reasons.append("vision")

    score = round(min(score, 1.0), 2)

    return score, reasons