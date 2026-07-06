from dataclasses import dataclass, field


@dataclass
class ImageCandidate:

    path: str
    page_no: int

    width: int
    height: int

    bbox: tuple = None

    source: str = "layout"

    category: str = "figure"

    image_type: str = ""

    area: int = 0

    caption: str = ""

    ocr_text: str = ""

    title: str = ""

    vision: str = ""

    page_text: str = ""

    page_context: str = ""

    search_text: str = ""

    clip_embedding: list = field(default_factory=list)

    image_hash: str = ""

    confidence_score: float = 0.0

    classification_confidence: float = 0.0

    source_file: str = ""

    file_type: str = ""

    filename: str = ""

    document_id: int = None