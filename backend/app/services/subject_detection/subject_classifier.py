from app.services.subject_detection.subject_detector import detect_subject
from app.services.subject_detection.groq_subject_service import (
    classify_subject_with_groq
)

HIGH_CONFIDENCE = 0.85
SAFE_MARGIN = 0.12


def classify_subject(preview_text):

    result = detect_subject(preview_text)

    matches = result["top_matches"]

    ##################################################
    # No matches
    ##################################################

    if len(matches) == 0:

        return {

            "primary_subject": None,

            "parent_subject": "",

            "confidence": 0,

            "matched_keywords": [],

            "secondary_subjects": [],

            "method": "none"

        }

    ##################################################
    # Best match
    ##################################################

    best = matches[0]

    ##################################################
    # Similarity margin
    ##################################################

    second_score = 0

    if len(matches) > 1:

        second_score = matches[1]["score"]

    margin = best["score"] - second_score

    ##################################################
    # Secondary subjects
    ##################################################

    secondary = [

        item["subject"]

        for item in matches[1:]

        if item["score"] >= 0.75

    ]

    ##################################################
    # Debug
    ##################################################

    print("\n========== SUBJECT DETECTION ==========")

    for item in matches[:10]:

        print(

            f"{item['subject']}"

            f" | {item['score']}"

        )

    print("Margin :", round(margin, 4))

    ##################################################
    # High confidence
    ##################################################

    if (

        best["score"] >= HIGH_CONFIDENCE

        or

        margin >= SAFE_MARGIN

    ):

        return {

            "primary_subject": best["subject"],

            "parent_subject": best["parent_subject"],

            "confidence": round(best["score"] * 100, 2),

            "matched_keywords": [],

            "secondary_subjects": secondary,

            "method": "embedding"

        }

    ##################################################
    # Low confidence -> Groq
    ##################################################

    print("Calling Groq...")

    return classify_subject_with_groq(

        preview_text,

        matches

    )