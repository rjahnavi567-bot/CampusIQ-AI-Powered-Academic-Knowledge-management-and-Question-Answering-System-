import re

STOPWORDS = {
    "a", "an", "the", "of", "for", "to", "and",
    "showing", "illustration", "image", "picture"
}


def clean_text(text):
    text = re.sub(r"[^A-Za-z0-9 ]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def generate_diagram_title(caption, ocr_text):
    """
    Generate a short academic title locally.
    No API call.
    """

    text = f"{caption} {ocr_text}"

    text = clean_text(text)

    words = []

    for word in text.split():

        word = word.lower()

        if word in STOPWORDS:
            continue

        if len(word) <= 2:
            continue

        words.append(word)

    if not words:
        return "Academic Diagram"

    title = " ".join(words[:6]).title()

    return title