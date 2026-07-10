def score_vision(images):

    print("\n==============================")
    print("VISION SCORER")
    print("==============================")

    for image in images:

        positive = [

            image.diagram_score,

            image.flowchart_score,

            image.table_score,

            image.graph_score,

            image.chart_score,

            image.equation_score,

            image.photo_score

        ]

        negative = [

            image.paragraph_score,

            image.heading_score,

            image.logo_score,

            image.icon_score,

            image.handwritten_score,

            image.screenshot_score

        ]

        positive_score = sum(positive) / len(positive)

        negative_score = sum(negative) / len(negative)

        image.vision_score = max(

            0.0,

            min(

                1.0,

                positive_score - 0.5 * negative_score

            )

        )

    print(f"Vision scored : {len(images)}")

    print("\nSample\n")

    for image in images[:5]:

        print(

            f"Page {image.page_no} | "

            f"Vision={image.vision_score:.3f}"

        )

    return images