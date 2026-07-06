from dataclasses import dataclass


@dataclass
class ImageCandidate:
    path: str
    page_no: int

    category: str

    bbox: tuple

    width: int
    height: int

    source: str = "layout"

    caption: str = ""
    ocr_text: str = ""
    title: str = ""
    vision: str = ""

    clip_embedding = None

    image_hash = ""

    confidence_score = 0

    classification_confidence = 0

    page_text = ""

    source_file = ""

    file_type = ""

    document_id = None