ACADEMIC_KEYWORDS = {

    "architecture":8,
    "diagram":8,
    "figure":7,
    "workflow":7,
    "flowchart":7,
    "algorithm":8,
    "pipeline":8,
    "process":6,
    "framework":8,
    "system":6,
    "network":7,
    "module":5,
    "component":5,
    "table":6,
    "graph":6,
    "chart":6,
    "equation":6,
    "formula":6,
    "example":3,
    "experiment":5,
    "result":5,
    "analysis":5,
    "comparison":5,
    "performance":5,
    "classification":5,
    "training":4,
    "testing":4,
    "accuracy":4

}


NEGATIVE_KEYWORDS = {

    "copyright":-10,
    "isbn":-10,
    "publisher":-8,
    "page":-3,
    "contents":-5,
    "index":-5,
    "preface":-5

}


def compute_context_score(image):

    text = image.page_context.lower()

    score = 0

    for word,value in ACADEMIC_KEYWORDS.items():

        if word in text:

            score += value

    for word,value in NEGATIVE_KEYWORDS.items():

        if word in text:

            score += value

    score = max(0,min(score,30))

    image.context_score = score

    return image


def analyze_context(images):

    print("\n==============================")
    print("CONTEXT ANALYZER")
    print("==============================")

    for image in images:

        compute_context_score(image)

    print(f"Context analyzed : {len(images)}")

    print("\nSample\n")

    for image in images[:10]:

        print(

            f"Page {image.page_no} | "
            f"Context Score={image.context_score}"

        )

    return images