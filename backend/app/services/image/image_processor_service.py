import os

from app.services.image_understanding_service import understand_image
from app.services.image_complexity_service import needs_groq_vision
from app.services.groq_decision_service import should_use_groq
from app.services.groq_vision_service import analyze_image

from app.services.image.image_metadata_service import build_metadata
from app.services.image_classifier_service import classify_image
from app.services.image_confidence_service import calculate_confidence


REJECT_WORDS = [

    "page of text",
    "text document",
    "paragraph",
    "printed text",
    "book page",
    "document page",
    "page containing text",
    "scanned page",
    "screenshot",
    "website",
    "article",
    "newspaper",
    "person",
    "people",
    "portrait",
    "face",
    "logo",
    "icon",
    "animal",
    "tree",
    "building",
    "landscape"

]


def process_single_image(image, page_lookup):

    understanding = understand_image(
        image["path"]
    )

    caption = understanding["caption"].lower()

    if any(word in caption for word in REJECT_WORDS):
        print(
    f"Rejected {image['path']} : caption"
)

        return None

    image["caption"] = understanding["caption"]
    image["ocr_text"] = understanding["ocr_text"]

    ocr_words = len(image["ocr_text"].split())

    caption = image["caption"].lower()

    if (
    ocr_words > 300
    and
    (
        "page of text" in caption
        or
        "document page" in caption
        or
        "printed text" in caption
        or
        "scanned page" in caption
    )
):

        print(
        f"Rejected {image['path']} : text page ({ocr_words} words)"
    )
  
        return None

    image = build_metadata(
        image,
        page_lookup
    )

    if (
        needs_groq_vision(
            image["caption"],
            image["ocr_text"]
        )
        or
        should_use_groq(image)
    ):

        try:

            image["vision"] = analyze_image(
                image["path"]
            )

        except Exception:

            image["vision"] = ""

    else:

        image["vision"] = ""

    # ---------------------------------------------------------
# Classify image first
# ---------------------------------------------------------

    cls = classify_image(

    title=image["title"],
    caption=image["caption"],
    ocr=image["ocr_text"],
    page_text=image["page_text"]

)

    image["category"] = cls["category"]
    image["classification_confidence"] = cls["confidence"]

# ---------------------------------------------------------
# Now confidence can use classifier confidence
# ---------------------------------------------------------

    score, reasons = calculate_confidence(
    image
)

    image["confidence_score"] = score
    image["confidence_reasons"] = ",".join(reasons)

    if score < 0.45:

        print(
        f"Rejected {image['path']} : confidence {score}"
    )

        return None

    return image