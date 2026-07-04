import re

# ---------------------------------------------------------
# Academic Image Classifier
# ---------------------------------------------------------

CATEGORY_RULES = {

    "Block Diagram": [
        "block diagram",
        "architecture",
        "system architecture",
        "cpu",
        "processor",
        "memory",
        "register",
        "cache",
        "bus",
        "module"
    ],

    "Flowchart": [
        "flowchart",
        "flow chart",
        "workflow",
        "decision",
        "process flow",
        "algorithm flow"
    ],

    "Circuit Diagram": [
        "circuit",
        "resistor",
        "capacitor",
        "transistor",
        "voltage",
        "current",
        "electrical",
        "schematic"
    ],

    "Graph": [
        "graph",
        "plot",
        "curve",
        "accuracy",
        "loss",
        "performance",
        "precision",
        "recall",
        "roc",
        "bar chart",
        "line chart",
        "scatter"
    ],

    "Table": [
        "table",
        "tabulation",
        "comparison table"
    ],

    "Network Diagram": [
        "network",
        "topology",
        "client",
        "server",
        "router",
        "switch"
    ],

    "Architecture Diagram": [
        "architecture",
        "framework",
        "pipeline",
        "workflow",
        "system design",
        "microservice"
    ],

    "Mathematical Figure": [
        "equation",
        "formula",
        "proof",
        "theorem",
        "geometry",
        "triangle",
        "integral",
        "matrix"
    ],

    "Chemical Structure": [
        "molecule",
        "chemical",
        "compound",
        "benzene",
        "reaction",
        "atom"
    ]
}


def classify_image(
    title="",
    caption="",
    ocr="",
    page_text=""
):
    """
    Returns

    category
    confidence
    """

    text = " ".join([
        title,
        caption,
        ocr,
        page_text[:500]
    ]).lower()

    text = re.sub(r"\s+", " ", text)

    scores = {}

    for category, keywords in CATEGORY_RULES.items():

        score = 0

        for keyword in keywords:

            if keyword in text:
                score += 1

        scores[category] = score

    best_category = "Generic Diagram"

    confidence = 0.50

    if max(scores.values()) > 0:

        best_category = max(
            scores,
            key=scores.get
        )

        confidence = min(
            0.60 + scores[best_category] * 0.08,
            0.98
        )

    return {

        "category": best_category,

        "confidence": round(confidence, 2)

    }