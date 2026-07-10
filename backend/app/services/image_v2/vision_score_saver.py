# --------------------------------------------------
# Save Vision Scores
# --------------------------------------------------

def save_vision_scores(images):

    print("\n==============================")
    print("VISION SCORE SAVER")
    print("==============================")

    mapping = {

    "diagram": "diagram_score",

    "flowchart": "flowchart_score",

    "graph": "graph_score",

    "chart": "chart_score",

    "table": "table_score",

    "photo": "photo_score",

    "equation": "equation_score",

    "chemical": "chemical_score",

    "medical": "medical_score",

    "paragraph": "paragraph_score",

    "heading": "paragraph_score",

    "logo": "logo_score",

    "icon": "icon_score",

    "watermark": "logo_score",

    "handwritten": "handwritten_score",

    "screenshot": "screenshot_score",

}

    for image in images:

        if not image.vision_scores:
            continue

        for category, attribute in mapping.items():

            setattr(

        image,

        attribute,

        image.vision_scores.get(

            category,

            0.0

        )

    )

    print(f"Vision scores saved : {len(images)}")

    print("\nSample")

    for image in images[:5]:

        print(

            f"Page {image.page_no} | "

            f"Diagram={image.diagram_score:.2f} | "

            f"Photo={image.photo_score:.2f} | "

            f"Paragraph={image.paragraph_score:.2f}"

        )

    return images