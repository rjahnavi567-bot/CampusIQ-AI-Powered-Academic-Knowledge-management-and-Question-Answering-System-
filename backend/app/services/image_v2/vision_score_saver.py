# --------------------------------------------------
# Save Vision Scores
# --------------------------------------------------

def save_vision_scores(images):

    print("\n==============================")
    print("VISION SCORE SAVER")
    print("==============================")

    mapping = {

        "a diagram": "diagram_score",

        "a flowchart": "flowchart_score",

        "a graph": "graph_score",

        "a chart": "chart_score",

        "a table": "table_score",

        "a photograph": "photo_score",

        "a person": "person_score",

        "a logo": "logo_score",

        "an icon": "icon_score",

        "a paragraph of text": "paragraph_score",

        "a page full of text": "text_page_score",

        "a handwritten note": "handwritten_score",

        "a screenshot": "screenshot_score",

        "a microscope image": "microscope_score",

        "a medical image": "medical_score",

        "a chemical structure": "chemical_score",

        "a mathematical equation": "equation_score"

    }

    for image in images:

        if not image.vision_scores:
            continue

        for prompt, attribute in mapping.items():

            setattr(

                image,

                attribute,

                image.vision_scores.get(

                    prompt,

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