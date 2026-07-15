from .geometry import iou


MIN_AREA_RATIO = 0.003
MAX_AREA_RATIO = 0.85

MERGE_DISTANCE = 30

EXPAND_PIXELS = 12
def area(box):

    x1, y1, x2, y2 = box

    return max(0, x2 - x1) * max(0, y2 - y1)

def expand_box(box, width, height):

    x1, y1, x2, y2 = box

    x1 = max(0, x1 - EXPAND_PIXELS)
    y1 = max(0, y1 - EXPAND_PIXELS)

    x2 = min(width, x2 + EXPAND_PIXELS)
    y2 = min(height, y2 + EXPAND_PIXELS)

    return (x1, y1, x2, y2)

def clip_box(box, width, height):

    x1, y1, x2, y2 = box

    return (

        max(0, x1),

        max(0, y1),

        min(width, x2),

        min(height, y2)

    )

def merge_boxes(box1, box2):

    return (

        min(box1[0], box2[0]),

        min(box1[1], box2[1]),

        max(box1[2], box2[2]),

        max(box1[3], box2[3])

    )

def boxes_close(box1, box2):

    ax1, ay1, ax2, ay2 = box1
    bx1, by1, bx2, by2 = box2

    if iou(box1, box2) > 0:
        return True

    horizontal = max(bx1 - ax2, ax1 - bx2, 0)

    vertical = max(by1 - ay2, ay1 - by2, 0)

    return horizontal < MERGE_DISTANCE and vertical < MERGE_DISTANCE
def refine_regions(detections, image):

    height, width = image.shape[:2]

    page_area = width * height

    refined = []

    # -----------------------------------
    # Step 1 : Clip + Remove tiny regions
    # -----------------------------------

    for det in detections:

        box = clip_box(det["bbox"], width, height)

        if area(box) / page_area < MIN_AREA_RATIO:
            continue

        det["bbox"] = box

        refined.append(det)

    # -----------------------------------
    # Step 2 : Remove page-sized regions
    # -----------------------------------

    filtered = []

    for det in refined:

        if area(det["bbox"]) / page_area > MAX_AREA_RATIO:
            continue

        filtered.append(det)

    refined = filtered

    # -----------------------------------
    # Step 3 : Merge nearby fragments
    # -----------------------------------

    merged = []

    while refined:

        current = refined.pop(0)

        changed = True

        while changed:

            changed = False

            for other in refined[:]:

                if boxes_close(
                    current["bbox"],
                    other["bbox"]
                ):

                    current["bbox"] = merge_boxes(
                        current["bbox"],
                        other["bbox"]
                    )

                    refined.remove(other)

                    changed = True

        merged.append(current)

    # -----------------------------------
    # Step 4 : Expand boxes slightly
    # -----------------------------------

    for det in merged:

        det["bbox"] = expand_box(
            det["bbox"],
            width,
            height
        )

    print(f"Region refinement : {len(merged)}")

    return merged