from PIL import Image
import imagehash


PHASH_THRESHOLD = 6


def compute_hash(path):
    return imagehash.phash(Image.open(path))


def remove_duplicates(images):
    """
    images = list of dictionaries
    """

    accepted = []

    hashes = []

    for image in images:

        h = compute_hash(image.path)

        duplicate = False

        for old in hashes:

            if h - old <= PHASH_THRESHOLD:
                duplicate = True
                break

        if duplicate:
            continue

        hashes.append(h)

        image.image_hash = str(h)

        accepted.append(image)

    return accepted