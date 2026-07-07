import cv2
import numpy as np


# ----------------------------------------------------
# Region Proposal Parameters
# ----------------------------------------------------

MIN_REGION_AREA = 12000

MAX_PAGE_RATIO = 0.90

MAX_ASPECT_RATIO = 8.0

DILATION_KERNEL = (7, 7)

DILATION_ITERATIONS = 2


###########################################################
# Region Detector
###########################################################

def detect_regions(page_image):

    """
    Generate additional visual-region proposals that
    PPStructure may have missed.

    Input:
        page_image (BGR)

    Output:
        [
            {
                "bbox": (x1,y1,x2,y2),
                "category":"region",
                "confidence":0.50
            }
        ]
    """

    gray = cv2.cvtColor(
        page_image,
        cv2.COLOR_BGR2GRAY
    )

    ####################################################
    # Binary Image
    ####################################################

    binary = cv2.adaptiveThreshold(

        gray,

        255,

        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,

        cv2.THRESH_BINARY_INV,

        31,

        15

    )

    ####################################################
    # Merge Nearby Objects
    ####################################################

    kernel = cv2.getStructuringElement(

        cv2.MORPH_RECT,

        DILATION_KERNEL

    )

    merged = cv2.dilate(

        binary,

        kernel,

        iterations=DILATION_ITERATIONS

    )

    ####################################################
    # Find Contours
    ####################################################

    contours, _ = cv2.findContours(

        merged,

        cv2.RETR_EXTERNAL,

        cv2.CHAIN_APPROX_SIMPLE

    )

    page_height, page_width = page_image.shape[:2]

    page_area = page_height * page_width

    detections = []

    ####################################################
    # Region Filtering
    ####################################################

    for contour in contours:

        x, y, w, h = cv2.boundingRect(contour)

        area = w * h

        # Ignore tiny regions
        if area < MIN_REGION_AREA:
            continue

        # Ignore almost entire page
        if area > page_area * MAX_PAGE_RATIO:
            continue

        # Ignore long text strips
        aspect = max(w / h, h / w)

        if aspect > MAX_ASPECT_RATIO:
            continue

        detections.append(

            {

                "bbox": (
                    x,
                    y,
                    x + w,
                    y + h
                ),

                "category": "region",

                "confidence": 0.50

            }

        )

    print(f"Region proposals : {len(detections)}")

    return detections