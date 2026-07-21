import math
from .caption_ocr import read_caption

def box_distance(box1, box2):
    """
    Vertical distance between two boxes.
    """

    _, _, _, y2 = box1
    _, y1, _, _ = box2

    return abs(y1 - y2)


def merge_captions(regions):
    """
    Merge captions with nearest figure/table.

    Returns updated regions.
    """

    figures = []
    captions = []

    for r in regions:

        label = r.get("label", r.get("category"))

        if label in ["figure", "table"]:

            r["caption"] = ""

            figures.append(r)

        elif label in ["figure_caption", "table_caption"]:

            captions.append(r)

    # ----------------------------------------

    for caption in captions:

        caption_box = caption["bbox"]

        best = None

        best_distance = 999999

        for figure in figures:

            figure_box = figure["bbox"]

            d = box_distance(
                figure_box,
                caption_box
            )

            if d < best_distance:

                best_distance = d

                best = figure

        if best is not None:

            best["caption_bbox"] = caption_box

            best["caption_path"] = caption["path"]

            try:

                best["caption"] = read_caption(
        caption["path"]
    )

            except:

                best["caption"] = ""

    return figures