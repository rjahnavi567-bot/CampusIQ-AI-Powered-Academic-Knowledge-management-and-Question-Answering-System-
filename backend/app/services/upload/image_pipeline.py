import os
import hashlib
import re
import glob
import cv2
from app.services.image_extraction_service import (
    extract_pdf_images,
    extract_docx_images,
    extract_pptx_images,
    extract_image_file,
    extract_images
)

from app.services.image_understanding_service import (
    understand_image
)

from app.services.groq_vision_service import (
    analyze_image
)

from app.services.image_embedding_service import (
    embed_image
)

from app.services.image_context_service import (
    get_page_text
)
from app.services.diagram_title_service import (
    generate_diagram_title
)

# ---------------------------------------------------------
# Duplicate Removal
# ---------------------------------------------------------

def remove_duplicate_images(images):

    unique = []

    hashes = set()

    for image in images:

        try:

            with open(image["path"], "rb") as f:

                h = hashlib.md5(f.read()).hexdigest()

            if h in hashes:

                os.remove(image["path"])

                continue

            hashes.add(h)

            unique.append(image)

        except Exception:

            unique.append(image)

    return unique


# ---------------------------------------------------------
# Image Processing Pipeline
# ---------------------------------------------------------

def process_images(
    file_path,
    document_id,
    pages,
    source_file
):

    extension = os.path.splitext(
        file_path
    )[1].lower()

    page_lookup = {

        page["page_no"]: page["text"]

        for page in pages

    }

    # -----------------------------------------------------
    # Extract Images
    # -----------------------------------------------------

    if extension == ".pdf":

        images = extract_pdf_images(
            file_path,
            document_id
        )

    elif extension == ".docx":

        images = extract_docx_images(
            file_path,
            document_id
        )

    elif extension == ".pptx":

        images = extract_pptx_images(
            file_path,
            document_id
        )

    elif extension in [

        ".png",

        ".jpg",

        ".jpeg"

    ]:

        images = extract_image_file(
            file_path
        )

    else:

        images = extract_images(
            file_path,
            document_id
        )

    # -----------------------------------------------------
    # Remove duplicates
    # -----------------------------------------------------

    images = remove_duplicate_images(images)

    print()

    print("Unique Images :", len(images))

    print()

    # -----------------------------------------------------
    # Understand every image
    # -----------------------------------------------------

    processed = []

    for image in images:

        if not os.path.exists(image["path"]):

            continue

        # Ignore useless images

        if not is_useful_image(image["path"]):

          try:
             os.remove(image["path"])
          except:
             pass

          continue

        understanding = understand_image(

            image["path"]

        )
        caption = understanding["caption"].lower()

        bad_words = [

    "person",

    "people",

    "portrait",

    "face",

    "building",

    "tree",

    "landscape",

    "animal"

]

        if any(

    word in caption

    for word in bad_words

):

            try:
                os.remove(image["path"])
            except:
                pass

            continue

        image["caption"] = understanding["caption"]

        image["ocr_text"] = understanding["ocr_text"]

        # -----------------------------------
        # Academic Diagram Title
        # -----------------------------------

        image["title"] = generate_diagram_title(

    image["caption"],

    image["ocr_text"]

)

        try:

            image["vision"] = analyze_image(

                image["path"]

            )

        except Exception:

            image["vision"] = ""

        image["page_text"] = get_page_text(

            page_lookup,

            image["page_no"]

        )

        image["source_file"] = source_file

        image["file_type"] = os.path.splitext(

            source_file

        )[1].lower()

        image["document_id"] = document_id
        # -----------------------------------
        # Rename image using title + page + hash
        # -----------------------------------

        try:

            image_hash = generate_image_hash(image["path"])

            safe_title = clean_filename(image["title"])

            extension = os.path.splitext(image["path"])[1]

            new_name = (

        f"{safe_title}"

        f"_p{image['page_no']}"

        f"_{image_hash}"

        f"{extension}"

    )

            new_path = os.path.join(

        os.path.dirname(image["path"]),

        new_name

    )

            if image["path"] != new_path:

                os.rename(

            image["path"],

            new_path

        )

                image["path"] = new_path

            image["image_hash"] = image_hash

        except Exception as e:

            print("Rename Error:", e)

        # -----------------------------------------
        # CLIP Embedding
        # -----------------------------------------

        try:

            image["clip_embedding"] = embed_image(

                image["path"]

            )

        except Exception:

            image["clip_embedding"] = None
        
        duplicate = False

        for old in processed:

            same_title = (

    old["title"].lower().strip()

    == image["title"].lower().strip()

)

            same_hash = (

    old["image_hash"]

    == image["image_hash"]

)

            if same_hash or (

    same_title

    and

    abs(

        old["page_no"]

        - image["page_no"]

    ) <= 1

):

                duplicate = True
                break

        if duplicate:

            try:
                os.remove(image["path"])
            except:
                pass

            continue

        processed.append(image)
  

    page_images = glob.glob(
    f"uploads/images/{document_id}/page_*.png"
)

    for img in page_images:
      if os.path.exists(img):

        try:
           os.remove(img)
        except:
           pass

    return processed

def clean_filename(name):

    name = name.lower()

    name = re.sub(r"[^a-z0-9 ]", "", name)

    name = name.replace(" ", "_")

    while "__" in name:
        name = name.replace("__", "_")

    return name[:80]


def generate_image_hash(image_path):

    sha = hashlib.sha256()

    with open(image_path, "rb") as f:

        while True:

            data = f.read(8192)

            if not data:
                break

            sha.update(data)

    return sha.hexdigest()[:8]

def is_useful_image(image_path):
    """
    Remove logos, tiny icons, blank images,
    photographs and decorative graphics.
    Keep only academic diagrams.
    """

    image = cv2.imread(image_path)

    if image is None:
        return False

    h, w = image.shape[:2]

    # Too small
    if w < 180 or h < 180:
        return False

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    edges = cv2.Canny(
        gray,
        80,
        180
    )

    edge_pixels = cv2.countNonZero(edges)

    ratio = edge_pixels / (w * h)

    # Blank images
    if ratio < 0.01:
        return False

    # Very dense natural photos
    if ratio > 0.45:
        return False

    return True