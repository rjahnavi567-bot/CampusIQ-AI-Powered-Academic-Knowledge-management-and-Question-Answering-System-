from PIL import Image
import imagehash
import os

PHASH_THRESHOLD = 6
IOU_THRESHOLD = 0.80


#########################################################


def compute_hash(path):

    return imagehash.phash(
        Image.open(path)
    )


#########################################################


def compute_iou(box1, box2):

    if box1 is None or box2 is None:
        return 0

    x1, y1, x2, y2 = box1
    a1, b1, a2, b2 = box2

    xx1 = max(x1, a1)
    yy1 = max(y1, b1)
    xx2 = min(x2, a2)
    yy2 = min(y2, b2)

    if xx2 <= xx1 or yy2 <= yy1:
        return 0

    inter = (xx2 - xx1) * (yy2 - yy1)

    area1 = (x2 - x1) * (y2 - y1)
    area2 = (a2 - a1) * (b2 - b1)

    union = area1 + area2 - inter

    return inter / union


#########################################################


def remove_duplicates(images):

    accepted = []

    hashes = []

    removed_hash = 0
    removed_iou = 0

    for image in images:

        ########################################
        # pHash duplicate
        ########################################

        try:

            h = compute_hash(image.path)

        except Exception:

            continue

        duplicate = False

        for old in hashes:

            if h - old <= PHASH_THRESHOLD:

                duplicate = True
                break

        if duplicate:

            removed_hash += 1

            try:

                os.remove(image.path)

            except:
                pass

            continue

        ########################################
        # IoU duplicate
        ########################################

        overlap = False

        for existing in accepted:

            if image.page_no != existing.page_no:
                continue

            if image.bbox is None:
                continue

            if existing.bbox is None:
                continue

            iou = compute_iou(
                image.bbox,
                existing.bbox
            )

            if iou > IOU_THRESHOLD:

                overlap = True

                if image.area > existing.area:

                    try:
                        os.remove(existing.path)
                    except:
                        pass

                    accepted.remove(existing)

                    break

                else:

                    try:
                        os.remove(image.path)
                    except:
                        pass

                    removed_iou += 1
                    overlap = True
                    break

        if overlap and image not in accepted:

            if any(
                compute_iou(image.bbox, x.bbox) > IOU_THRESHOLD
                for x in accepted
                if x.page_no == image.page_no
            ):
                continue

        image.image_hash = str(h)

        hashes.append(h)

        accepted.append(image)

    print("\n========== DUPLICATE FILTER ==========")
    print(f"Input Images      : {len(images)}")
    print(f"Removed by pHash  : {removed_hash}")
    print(f"Removed by IoU    : {removed_iou}")
    print(f"Final Images      : {len(accepted)}")
    print("======================================\n")

    return accepted