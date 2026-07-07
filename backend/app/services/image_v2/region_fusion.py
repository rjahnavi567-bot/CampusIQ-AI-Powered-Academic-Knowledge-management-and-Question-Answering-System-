"""
Stage 4
--------

Merge PPStructure detections with Region Detector detections.

Pipeline

PPStructure
        +
Region Detector
        ↓
 Region Fusion
        ↓
Final Regions

"""

# --------------------------------------------------
# IoU Threshold
# --------------------------------------------------

IOU_THRESHOLD = 0.40


# --------------------------------------------------
# IoU Calculation
# --------------------------------------------------

def calculate_iou(box1, box2):
    """
    box = (x1,y1,x2,y2)
    """

    x_left = max(box1[0], box2[0])
    y_top = max(box1[1], box2[1])

    x_right = min(box1[2], box2[2])
    y_bottom = min(box1[3], box2[3])

    if x_right <= x_left:
        return 0.0

    if y_bottom <= y_top:
        return 0.0

    intersection = (
        (x_right - x_left) *
        (y_bottom - y_top)
    )

    area1 = (
        (box1[2] - box1[0]) *
        (box1[3] - box1[1])
    )

    area2 = (
        (box2[2] - box2[0]) *
        (box2[3] - box2[1])
    )

    union = area1 + area2 - intersection

    if union <= 0:
        return 0.0

    return intersection / union


# --------------------------------------------------
# Check Overlap
# --------------------------------------------------

def overlaps(existing_boxes, candidate_box):

    for box in existing_boxes:

        if calculate_iou(
            box["bbox"],
            candidate_box["bbox"]
        ) >= IOU_THRESHOLD:

            return True

    return False


# --------------------------------------------------
# Region Fusion
# --------------------------------------------------

def fuse_regions(layout_regions, cv_regions):
    """
    Inputs
    ------
    layout_regions :
        PPStructure detections

    cv_regions :
        OpenCV detections

    Output
    ------
    Final merged detections
    """

    print("\nStage 4 : Region Fusion")

    fused = []

    # ---------------------------------------------
    # Step 1
    # Keep ALL PPStructure detections
    # ---------------------------------------------

    fused.extend(layout_regions)

    # ---------------------------------------------
    # Step 2
    # Add only new OpenCV detections
    # ---------------------------------------------

    added = 0

    skipped = 0

    for region in cv_regions:

        if overlaps(fused, region):

            skipped += 1

            continue

        fused.append(region)

        added += 1

    print(f"Layout Regions : {len(layout_regions)}")
    print(f"Region Detector: {len(cv_regions)}")
    print(f"Added          : {added}")
    print(f"Skipped        : {skipped}")
    print(f"Final Regions  : {len(fused)}")

    return fused