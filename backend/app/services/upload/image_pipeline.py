import os
import hashlib
import re
import glob
import cv2
import numpy as np
from app.services.image_extraction_service import (
    extract_pdf_images,
    extract_docx_images,
    extract_pptx_images,
    extract_image_file,
    extract_images
)
from app.services.groq_decision_service import should_use_groq
from app.services.image_classifier_service import classify_image
from app.services.figure_title_service import (
    extract_figure_title
)
from app.services.image_understanding_service import (
    understand_image
)
from app.services.image_complexity_service import needs_groq_vision
from app.services.groq_vision_service import (
    analyze_image
)

from app.services.image_embedding_service import (
    embed_images,embed_image
)

from app.services.image_context_service import (
    get_page_text
)
from app.services.diagram_title_service import (
    generate_diagram_title
)
from app.services.image_confidence_service import (
    calculate_confidence
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

        reject_words = [

    "page of text",

    "text document",

    "paragraph",

    "printed text",

    "book page",

    "document page",

    "page containing text",

    "scanned page",

    "screenshot",

    "website",

    "article",

    "newspaper",

    "person",

    "people",

    "portrait",

    "face",

    "logo",

    "icon",

    "animal",

    "tree",

    "building",

    "landscape"

]

        if any(word in caption for word in reject_words):

            try:
                os.remove(image["path"])
            except:
                pass

            continue

        image["caption"] = understanding["caption"]

        image["ocr_text"] = understanding["ocr_text"]
        ocr_words = len(image["ocr_text"].split())

        if ocr_words > 120:

            try:
                os.remove(image["path"])
            except:
                pass

            continue

        # -----------------------------------
        # Academic Diagram Title
        # -----------------------------------

        # -----------------------------------
# Try extracting textbook figure title
# -----------------------------------

        page_text = get_page_text(

    page_lookup,

    image["page_no"]

)

        figure_title, confidence = extract_figure_title(

    page_text

)

        if figure_title:

            image["title"] = figure_title

            print(
        f"Figure title detected: {figure_title}"
    )

        else:

            image["title"] = generate_diagram_title(

        image["caption"],

        image["ocr_text"]

    )

        complex_image = needs_groq_vision(
    image["caption"],
    image["ocr_text"]
)

        use_groq = (
    complex_image or
    should_use_groq(image)
)
 
        if use_groq:

            print("Running Groq Vision...")

            try:

                image["vision"] = analyze_image(
            image["path"]
        )

            except Exception:

               image["vision"] = ""

        else:

            image["vision"] = ""

        image["page_text"] = page_text
        classification = classify_image(

    title=image["title"],

    caption=image["caption"],

    ocr=image["ocr_text"],

    page_text=image["page_text"]

)

        image["category"] = classification["category"]

        image["classification_confidence"] = classification["confidence"]
        print(

    f"Category: {image['category']} "

    f"({image['classification_confidence']})"

)


        score, reasons = calculate_confidence(image)


        image["confidence_score"] = score

        image["confidence_reasons"] = ",".join(reasons)

        print(

    f"Confidence: {score} | {reasons}"

)
        if score < 0.45:

            try:
                os.remove(image["path"])
            except:
                pass

            continue

        
        image["source_file"] = source_file

        image["file_type"] = os.path.splitext(

            source_file

        )[1].lower()

        image["document_id"] = document_id
        # -----------------------------------
        # Rename image using title + page + hash
        # -----------------------------------

        image_hash = generate_image_hash(image["path"])

        image["image_hash"] = image_hash

        safe_title = clean_filename(image["title"])

        extension = os.path.splitext(image["path"])[1]
        folder = os.path.dirname(image["path"])

        base = (
    f"{document_id}_"
    f"{safe_title}"
    f"_page{image['page_no']}"
    f"_{image_hash}"
)

        new_path = os.path.join(
    folder,
    base + extension
)

        counter = 1

        while os.path.exists(new_path):

            new_path = os.path.join(

        folder,

        f"{base}_{counter}{extension}"

    )

            counter += 1
        try:
                os.rename(
            image["path"],
            new_path
        )

                image["path"] = new_path

        except Exception as e:

            print("Rename Error:", e)

        
        duplicate = False

        for old in processed:

            same_title = (

    old["title"].lower().strip()

    == image["title"].lower().strip()

)

            same_hash = (

    old.get("image_hash")

    == image.get("image_hash")

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

        if image.get("image_hash"):

            processed.append(image)
    # -----------------------------------------
# Batch CLIP Embeddings
# -----------------------------------------

    print("\nGenerating CLIP embeddings in batch...")

    image_paths = [

    image["path"]

    for image in processed

]

    try:

        embeddings = embed_images(image_paths)

    except Exception:

        embeddings = []

        for path in image_paths:

            try:

                embeddings.append(
                embed_image(path)
            )

            except Exception:

                embeddings.append(None)

    for image, embedding in zip(processed, embeddings):

        image["clip_embedding"] = embedding

    print(f"Generated {len(processed)} CLIP embeddings.")
  

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

    image = cv2.imread(image_path)

    if image is None:
        return False

    h, w = image.shape[:2]

    # Too small
    if w < 180 or h < 180:
        return False

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Blank image

    std = np.std(gray)

    if std < 8:
        return False

    # Edge Density

    edges = cv2.Canny(gray, 80, 180)

    edge_ratio = cv2.countNonZero(edges) / (w * h)

    if edge_ratio < 0.01:
        return False

    if edge_ratio > 0.42:
        return False

    # White ratio

    white_ratio = np.sum(gray > 245) / (w * h)

    if white_ratio > 0.97:
        return False

    return True