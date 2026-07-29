from app.services.subject_detection.subject_detector import detect_subject
from app.services.subject_detection.groq_subject_service import (
    classify_subject_with_groq
)

EMBEDDING_THRESHOLD = 0.85


def classify_subject(preview_text):

    result = detect_subject(preview_text)

    matches = result["top_matches"]

    if len(matches) == 0:
        return {

    "primary_subject": None,

    "parent_subject": "",

    "confidence": 0,

    "matched_keywords": [],

    "secondary_subjects": [],

    "method": "none"

}

    best = matches[0]

    secondary = [

        item["subject"]

        for item in matches[1:]

        if item["score"] >= 0.75

    ]

    ####################################################
# High confidence
####################################################

    if best["score"] >= EMBEDDING_THRESHOLD:

        return {

    "primary_subject": best["subject"],

    "parent_subject": "",

    "confidence": round(best["score"] * 100, 2),

    "matched_keywords": [],

    "secondary_subjects": secondary,

    "method": "embedding"

}
####################################################
# Low confidence -> Groq
####################################################

    groq_result = classify_subject_with_groq(
    preview_text
)


    return groq_result