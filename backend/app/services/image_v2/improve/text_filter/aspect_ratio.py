MIN_RATIO = 0.12
MAX_RATIO = 8.0

MIN_WIDTH = 60
MIN_HEIGHT = 60


def aspect_ratio_stats(crop):

    h, w = crop.shape[:2]

    if h == 0 or w == 0:

        return {
            "aspect_ratio": 0,
            "reject": True
        }

    ratio = w / h

    reject = False

    if ratio > MAX_RATIO:
        reject = True

    if ratio < MIN_RATIO:
        reject = True

    if w < MIN_WIDTH:
        reject = True

    if h < MIN_HEIGHT:
        reject = True

    return {
        "aspect_ratio": ratio,
        "reject": reject
    }