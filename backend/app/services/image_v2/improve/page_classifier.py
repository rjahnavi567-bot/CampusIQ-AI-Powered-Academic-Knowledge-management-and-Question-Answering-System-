from .text_filter.ocr_density import is_text_heavy
from .text_filter.connected_components import too_many_components
from .text_filter.edge_density_filter import edge_density
from .text_filter.white_ratio import white_ratio


PAGE_AREA_THRESHOLD = 0.90


def classify_full_page(crop, page_shape):

    page_area = page_shape[0] * page_shape[1]

    crop_area = crop.shape[0] * crop.shape[1]

    area_ratio = crop_area / page_area

    if area_ratio < PAGE_AREA_THRESHOLD:

        return False

    text = is_text_heavy(crop)

    cc = too_many_components(crop)

    edge = edge_density(crop)

    white = white_ratio(crop)

    score = 0

    if text["reject"]:
        score += 2

    if cc["reject"]:
        score += 2

    if edge > 0.30:
        score += 1

    if white > 0.65:
        score += 1

    return score >= 4