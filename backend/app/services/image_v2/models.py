from dataclasses import dataclass, field


@dataclass
class ImageCandidate:

    # --------------------------------------------------
    # Basic Information
    # --------------------------------------------------

    path: str
    page_no: int

    width: int
    height: int

    bbox: tuple = None

    source: str = "layout"

    category: str = "figure"

    image_type: str = ""

    area: int = 0

    filename: str = ""

    source_file: str = ""

    file_type: str = ""

    document_id: int = None

    confidence_score: float = 0.0

    classification_confidence: float = 0.0

    # --------------------------------------------------
    # Text / Context
    # --------------------------------------------------

    caption: str = ""

# Florence-2 detailed caption
    florence_caption: str = ""
    semantic_scores: dict = field(default_factory=dict)

    title: str = ""

    ocr_text: str = ""

    page_text: str = ""

    page_context: str = ""

    search_text: str = ""

    vision: str = ""

    # --------------------------------------------------
    # Embeddings
    # --------------------------------------------------

    clip_embedding: list = field(default_factory=list)

    # ==================================================
    # Stage 1 : Metadata Analyzer
    # ==================================================

    aspect_ratio: float = 0.0

    file_size: int = 0

    page_ratio: float = 0.0

    orientation: str = ""

    resolution: tuple = (0, 0)

    # ==================================================
    # Stage 2 : Quality Analyzer
    # ==================================================

    blur_score: float = 0.0

    noise_score: float = 0.0

    white_ratio: float = 0.0

    black_ratio: float = 0.0

    edge_density: float = 0.0

    is_empty: bool = False

    background_only: bool = False

    # ==================================================
    # Stage 3 : OCR Metadata
    # ==================================================

    word_count: int = 0

    line_count: int = 0

    text_area_ratio: float = 0.0

    bullet_count: int = 0

    digit_count: int = 0

    uppercase_ratio: float = 0.0

    has_paragraph: bool = False

    has_heading: bool = False

    # ==================================================
    # Stage 4 : Layout Analyzer
    # ==================================================

    connected_components: int = 0

    contour_count: int = 0

    horizontal_lines: int = 0

    vertical_lines: int = 0

    line_density: float = 0.0

    layout_diagram_score: float = 0.0

    layout_table_score: float = 0.0

    layout_chart_score: float = 0.0

    layout_photo_score: float = 0.0

    layout_type: str = "unknown"

    # ==================================================
    # Stage 5 : Duplicate Detector
    # ==================================================

    md5_hash: str = ""

    perceptual_hash: str = ""

    duplicate_similarity: float = 0.0

    duplicate_method: str = ""

    is_duplicate: bool = False

    duplicate_of: str = ""

    # ==================================================
    # Stage 6 : Vision Classification
    # ==================================================

    vision_scores: dict = field(default_factory=dict)

    vision_class: str = ""

    vision_confidence: float = 0.0

    # --------------------------------------------------
    # Saved Vision Scores
    # --------------------------------------------------

    diagram_score: float = 0.0

    flowchart_score: float = 0.0

    graph_score: float = 0.0

    chart_score: float = 0.0

    table_score: float = 0.0

    photo_score: float = 0.0

    person_score: float = 0.0

    logo_score: float = 0.0

    icon_score: float = 0.0

    paragraph_score: float = 0.0

    text_page_score: float = 0.0

    handwritten_score: float = 0.0

    screenshot_score: float = 0.0

    microscope_score: float = 0.0

    medical_score: float = 0.0

    chemical_score: float = 0.0

    equation_score: float = 0.0

    # ==================================================
    # Stage 7 : Decision Engine
    # ==================================================

    keep_image: bool = True

    useful_score: float = 0.0

    metadata_score: float = 0.0

    quality_score: float = 0.0

    ocr_score: float = 0.0

    layout_score: float = 0.0

    vision_score: float = 0.0

    duplicate_score: float = 0.0

    hard_reject: bool = False

    decision_reason: str = ""

    decision_log: list = field(default_factory=list)