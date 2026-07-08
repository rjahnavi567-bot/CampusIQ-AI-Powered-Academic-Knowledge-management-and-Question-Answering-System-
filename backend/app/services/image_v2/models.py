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
    # --------------------------------------------------
# Metadata Analyzer (Stage 1)
# --------------------------------------------------

    aspect_ratio: float = 0.0

    file_size: int = 0

    page_ratio: float = 0.0

    orientation: str = ""

    resolution: tuple = (0, 0)
    # --------------------------------------------------
# Quality Metrics
# --------------------------------------------------

    blur_score: float = 0.0

    noise_score: float = 0.0

    white_ratio: float = 0.0

    black_ratio: float = 0.0

    edge_density: float = 0.0

    is_empty: bool = False

    background_only: bool = False
    ocr_text: str = ""

    word_count: int = 0

    line_count: int = 0

    text_area_ratio: float = 0.0

    bullet_count: int = 0

    digit_count: int = 0

    uppercase_ratio: float = 0.0

    has_paragraph: bool = False

    has_heading: bool = False
    # --------------------------------------------------
# Layout Analyzer
# --------------------------------------------------

    white_ratio: float = 0.0

    black_ratio: float = 0.0

    edge_density: float = 0.0
 
    connected_components: int = 0

    contour_count: int = 0

    horizontal_lines: int = 0

    vertical_lines: int = 0

    line_density: int = 0

    diagram_score: float = 0.0

    table_score: float = 0.0

    chart_score: float = 0.0

    photo_score: float = 0.0

    layout_type: str = "unknown"

    # --------------------------------------------------
# Duplicate Detector
# --------------------------------------------------

    md5_hash: str = ""

    perceptual_hash =None

    is_duplicate: bool = False

    duplicate_of: str = ""