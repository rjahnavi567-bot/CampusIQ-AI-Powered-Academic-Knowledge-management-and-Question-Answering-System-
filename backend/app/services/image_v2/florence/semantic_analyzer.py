import re

# --------------------------------------------------
# Keyword Dictionary
# --------------------------------------------------

CATEGORY_KEYWORDS = {

    "diagram": [
        "diagram",
        "block diagram",
        "workflow",
        "flowchart",
        "pipeline",
        "architecture",
        "network",
        "uml",
        "er diagram",
        "system",
        "component",
        "schematic"
    ],

    "table": [
        "table",
        "rows",
        "columns",
        "grid",
        "spreadsheet"
    ],

    "chart": [
        "chart",
        "graph",
        "plot",
        "bar chart",
        "pie chart",
        "histogram",
        "scatter"
    ],

    "equation": [
        "equation",
        "formula",
        "matrix",
        "integral",
        "mathematical"
    ],

    "photo": [
        "photo",
        "photograph",
        "person",
        "animal",
        "building",
        "machine",
        "equipment",
        "device",
        "laboratory",
        "microscope"
    ],

    "paragraph": [
        "paragraph",
        "document",
        "page of text",
        "text",
        "printed text",
        "sentence"
    ],

    "heading": [
        "heading",
        "title"
    ],

    "logo": [
        "logo",
        "brand"
    ],

    "icon": [
        "icon",
        "symbol"
    ],

    "watermark": [
        "watermark"
    ],

    "handwritten": [
        "handwritten"
    ],

    "screenshot": [
        "software",
        "window",
        "toolbar",
        "desktop",
        "application"
    ]
}
def score_category(text, keywords):

    text = text.lower()

    hits = 0

    for word in keywords:

        if re.search(r"\b" + re.escape(word) + r"\b", text):

            hits += 1

    return hits / len(keywords)
def analyze_image(image):

    caption = image.florence_caption.lower()

    scores = {}

    for category, keywords in CATEGORY_KEYWORDS.items():

        scores[category] = score_category(
            caption,
            keywords
        )

    image.semantic_scores = scores

    return image
def analyze_semantics(images):

    print("\n==============================")
    print("SEMANTIC ANALYZER")
    print("==============================")

    for image in images:

        analyze_image(image)

    print(f"Semantic analyzed : {len(images)}")

    print("\nSample\n")

    for image in images[:5]:

        print(f"Page {image.page_no}")

        print(image.florence_caption)

        print(image.semantic_scores)

        print()

    return images