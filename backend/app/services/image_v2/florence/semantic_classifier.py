# --------------------------------------------------
# Caption Classifier
# --------------------------------------------------
USEFUL_CLASSES = {

    "diagram": {

        "diagram":5,
        "block diagram":5,
        "architecture":4,
        "workflow":4,
        "flowchart":5,
        "pipeline":4,
        "system":3,
        "component":3,
        "network":3,
        "illustration":2,
        "schematic":4,
        "topology":4,
        "uml":5,
        "entity relationship":5,
        "er diagram":5,
        "class diagram":5,
        "sequence diagram":5

    },

    "table":{

        "table":5,
        "rows":2,
        "columns":2,
        "grid":2,
        "spreadsheet":4

    },

    "graph":{

        "graph":5,
        "plot":4,
        "scatter":4,
        "histogram":5,
        "line graph":5,
        "curve":2

    },

    "chart":{

        "chart":5,
        "bar chart":5,
        "pie chart":5,
        "line chart":5

    },

    "equation":{

        "equation":5,
        "formula":5,
        "matrix":3,
        "integral":4,
        "mathematical":3

    },

    "photo":{

        "photograph":5,
        "photo":5,
        "person":2,
        "machine":4,
        "equipment":4,
        "laboratory":4,
        "device":3,
        "microscope":4,
        "engine":2

    }

}

BAD_CLASSES = {

    "paragraph":{

        "paragraph":5,
        "text":3,
        "document":4,
        "page":2,
        "sentence":2,
        "printed":3

    },

    "heading":{

        "heading":5,
        "title":4

    },

    "logo":{

        "logo":5,
        "brand":3

    },

    "icon":{

        "icon":5,
        "symbol":2

    },

    "watermark":{

        "watermark":5

    },

    "handwritten":{

        "handwritten":5

    },

    "screenshot":{

        "screenshot":5,
        "toolbar":3,
        "window":3,
        "software":4,
        "desktop":3,
        "interface":3

    }

}
def compute_score(text, keyword_dict):

    obtained = 0
    maximum = sum(keyword_dict.values())

    for keyword, weight in keyword_dict.items():

        if keyword in text:

            obtained += weight

    return round(obtained / maximum,3)
def classify_image(image):

    caption = image.florence_caption.lower()

    # useful

    for category, words in USEFUL_CLASSES.items():

        score = compute_score(caption, words)

        setattr(image,f"{category}_score",score)

    # bad

    for category, words in BAD_CLASSES.items():

        score = compute_score(caption,words)

        setattr(image,f"{category}_score",score)

    return image
def classify_images(images):

    print("\n==============================")
    print("SEMANTIC CAPTION CLASSIFIER")
    print("==============================")

    for image in images:

        classify_image(image)

    print(f"Semantic classified : {len(images)}")

    print("\nSample\n")

    for image in images[:5]:

        print(f"Page {image.page_no}")
        print(image.florence_caption)

        print()

        print(f"Diagram    : {image.diagram_score:.2f}")
        print(f"Table      : {image.table_score:.2f}")
        print(f"Graph      : {image.graph_score:.2f}")
        print(f"Chart      : {image.chart_score:.2f}")
        print(f"Equation   : {image.equation_score:.2f}")
        print(f"Photo      : {image.photo_score:.2f}")

        print()

        print(f"Paragraph  : {image.paragraph_score:.2f}")
        print(f"Heading    : {image.heading_score:.2f}")
        print(f"Logo       : {image.logo_score:.2f}")
        print(f"Screenshot : {image.screenshot_score:.2f}")

        print("------------------------------------")

    return images
