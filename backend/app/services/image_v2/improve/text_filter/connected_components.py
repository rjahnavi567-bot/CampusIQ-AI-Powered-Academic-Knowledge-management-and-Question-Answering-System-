import cv2


# ------------------------------------
# Configuration
# ------------------------------------

MAX_COMPONENTS = 3500

MIN_COMPONENT_AREA = 5


def count_components(image):
    """
    Counts connected components in an image.

    Returns
    -------
    int
    """

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    _, thresh = cv2.threshold(

        gray,

        0,

        255,

        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU

    )

    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
        thresh,
        connectivity=8
    )

    count = 0

    for i in range(1, num_labels):

        area = stats[i, cv2.CC_STAT_AREA]

        if area >= MIN_COMPONENT_AREA:

            count += 1

    return count


def too_many_components(image):
    """
    Returns component statistics.
    """

    components = count_components(image)

    return {

        "components": components,

        "reject": components > MAX_COMPONENTS

    }