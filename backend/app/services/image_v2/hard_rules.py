# --------------------------------------------------
# Hard Rule 1
# Empty Image
# --------------------------------------------------

def reject_empty(image):

    if image.is_empty:

        image.keep_image = False

        image.hard_reject = True

        image.decision_reason = "Empty Image"

        image.decision_log.append("Rejected : Empty Image")

        return True

    return False


# --------------------------------------------------
# Hard Rule 2
# Background Only
# --------------------------------------------------

def reject_background(image):

    if image.background_only:

        image.keep_image = False

        image.hard_reject = True

        image.decision_reason = "Background Only"

        image.decision_log.append("Rejected : Background Only")

        return True

    return False


# --------------------------------------------------
# Hard Rule 3
# Exact Duplicate
# --------------------------------------------------

def reject_duplicate(image):

    if image.is_duplicate:

        image.keep_image = False

        image.hard_reject = True

        image.decision_reason = "Duplicate Image"

        image.decision_log.append("Rejected : Duplicate")

        return True

    return False


# --------------------------------------------------
# Hard Rule 4
# Tiny Images
# --------------------------------------------------

MIN_WIDTH = 60
MIN_HEIGHT = 60


def reject_small(image):

    if image.width < MIN_WIDTH:

        image.keep_image = False

        image.hard_reject = True

        image.decision_reason = "Small Width"

        image.decision_log.append("Rejected : Width")

        return True

    if image.height < MIN_HEIGHT:

        image.keep_image = False

        image.hard_reject = True

        image.decision_reason = "Small Height"

        image.decision_log.append("Rejected : Height")

        return True

    return False


# --------------------------------------------------
# Hard Rule 5
# Almost White
# --------------------------------------------------

WHITE_LIMIT = 0.995


def reject_white(image):

    if image.white_ratio > WHITE_LIMIT:

        image.keep_image = False

        image.hard_reject = True

        image.decision_reason = "Almost White"

        image.decision_log.append("Rejected : White")

        return True

    return False


# --------------------------------------------------
# Hard Rule 6
# Almost Black
# --------------------------------------------------

BLACK_LIMIT = 0.995


def reject_black(image):

    if image.black_ratio > BLACK_LIMIT:

        image.keep_image = False

        image.hard_reject = True

        image.decision_reason = "Almost Black"

        image.decision_log.append("Rejected : Black")

        return True

    return False


# --------------------------------------------------
# Apply All Rules
# --------------------------------------------------

def apply_hard_rules(images):

    print("\n==============================")
    print("HARD RULES")
    print("==============================")

    accepted = []

    rejected = 0

    for image in images:

        if reject_empty(image):

            rejected += 1

            continue

        if reject_background(image):

            rejected += 1

            continue

        if reject_duplicate(image):

            rejected += 1

            continue

        if reject_small(image):

            rejected += 1

            continue

        if reject_white(image):

            rejected += 1

            continue

        if reject_black(image):

            rejected += 1

            continue

        accepted.append(image)

    print(f"Accepted : {len(accepted)}")

    print(f"Rejected : {rejected}")

    return accepted