import re


COMPLEX_KEYWORDS = {

    "flow",

    "architecture",

    "pipeline",

    "network",

    "algorithm",

    "system",

    "framework",

    "process",

    "block",

    "cpu",

    "memory",

    "cache",

    "neural",

    "database",

    "graph",

    "chart",

    "sequence",

    "uml",

    "class"

}


def needs_groq_vision(caption, ocr_text):

    text = f"{caption} {ocr_text}".lower()

    if len(ocr_text.split()) > 30:
        return True

    for keyword in COMPLEX_KEYWORDS:

        if keyword in text:
            return True

    return False