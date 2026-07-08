from .image_hash import compute_md5
from .image_hash import compute_md5, compute_phash

def detect_exact_duplicates(images):

    print("\n==============================")
    print("EXACT DUPLICATE DETECTOR")
    print("==============================")

    unique_images = []

    md5_lookup = {}

    duplicates = 0

    for image in images:

        image.md5_hash = compute_md5(image.path)

        if image.md5_hash in md5_lookup:

            image.is_duplicate = True

            image.duplicate_of = md5_lookup[image.md5_hash]

            duplicates += 1

            continue

        md5_lookup[image.md5_hash] = image.path

        unique_images.append(image)

    print(f"Unique Images : {len(unique_images)}")
    print(f"Duplicates    : {duplicates}")

    return unique_images
PHASH_THRESHOLD = 6


def detect_similar_duplicates(images):

    print("\n==============================")
    print("SIMILAR DUPLICATE DETECTOR")
    print("==============================")

    unique = []

    removed = 0

    for image in images:

        image.perceptual_hash = compute_phash(image.path)

        duplicate = False

        for existing in unique:

            distance = image.perceptual_hash - existing.perceptual_hash

            if distance <= PHASH_THRESHOLD:

                image.is_duplicate = True

                image.duplicate_of = existing.path

                duplicate = True

                removed += 1

                break

        if not duplicate:

            unique.append(image)

    print(f"Unique Images : {len(unique)}")
    print(f"Similar Removed : {removed}")

    return unique