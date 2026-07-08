from .image_hash import compute_md5


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