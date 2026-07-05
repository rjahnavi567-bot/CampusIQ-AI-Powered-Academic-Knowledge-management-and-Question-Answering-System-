import fitz


def merge_rects(rects, margin=15):
    """
    Merge nearby rectangles into larger figure regions.
    """

    merged = []

    for rect in rects:

        expanded = fitz.Rect(
            rect.x0 - margin,
            rect.y0 - margin,
            rect.x1 + margin,
            rect.y1 + margin
        )

        found = False

        for i, old in enumerate(merged):

            if expanded.intersects(old):

                merged[i] = old | expanded
                found = True
                break

        if not found:
            merged.append(expanded)

    return merged


def extract_vector_figures(page):

    drawings = page.get_drawings()

    rects = []

    for drawing in drawings:

        rect = drawing.get("rect")

        if rect is None:
            continue

        if rect.width < 80:
            continue

        if rect.height < 80:
            continue

        rects.append(rect)

    return merge_rects(rects)