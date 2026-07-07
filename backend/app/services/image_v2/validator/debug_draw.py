import cv2


# --------------------------------------------
# Colors (BGR)
# --------------------------------------------

GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
RED = (0, 0, 255)


def draw_boxes(image, detections, color, title=None):
    """
    Draw bounding boxes on an image.

    Parameters
    ----------
    image : numpy.ndarray

    detections : list of dict
        Each detection must contain:
            detection["bbox"]

    color : tuple(B,G,R)

    title : optional text
    """

    canvas = image.copy()

    for det in detections:

        x1, y1, x2, y2 = map(int, det["bbox"])

        cv2.rectangle(
            canvas,
            (x1, y1),
            (x2, y2),
            color,
            3
        )

    if title is not None:

        cv2.putText(

            canvas,

            title,

            (20, 40),

            cv2.FONT_HERSHEY_SIMPLEX,

            1,

            color,

            2,

            cv2.LINE_AA

        )

    return canvas


# ----------------------------------------------------------
# Individual helpers
# ----------------------------------------------------------

def draw_layout(page_image, layout_boxes):

    return draw_boxes(

        page_image,

        layout_boxes,

        GREEN,

        "PPStructure"

    )


def draw_regions(page_image, region_boxes):

    return draw_boxes(

        page_image,

        region_boxes,

        BLUE,

        "Region Detector"

    )


def draw_fusion(page_image, fusion_boxes):

    return draw_boxes(

        page_image,

        fusion_boxes,

        RED,

        "Fusion Output"

    )