# --------------------------------------------------
# Stage 7.2
# Hard Decision Rules
# --------------------------------------------------


KEEP_WORDS = {

    "diagram",
    "architecture",
    "workflow",
    "flowchart",
    "pipeline",
    "network",
    "graph",
    "chart",
    "table",
    "equation",
    "formula",
    "algorithm",
    "machine",
    "equipment",
    "scientific",
    "microscope",
    "illustration"

}


REMOVE_WORDS = {

    "paragraph",
    "text only",
    "page of text",
    "document page",
    "heading",
    "title",
    "logo",
    "icon",
    "watermark",
    "copyright",
    "isbn",
    "publisher",
    "blank",
    "decorative",
    "toolbar",
    "menu",
    "application",
    "software screenshot"

}


# --------------------------------------------------
# One Image
# --------------------------------------------------

def apply_rules(image):

    image.hard_reject = False

    image.keep_image = True

    image.decision_reason = ""

    image.decision_log = []

    ###################################################
    # Duplicate
    ###################################################

    if image.is_duplicate:

        image.hard_reject = True
        image.keep_image = False

        image.decision_reason = "Duplicate image"

        image.decision_log.append("Duplicate")

        return image

    ###################################################
    # Empty Image
    ###################################################

    if image.is_empty:

        image.hard_reject = True
        image.keep_image = False

        image.decision_reason = "Empty image"

        image.decision_log.append("Empty")

        return image

    ###################################################
    # Background Only
    ###################################################

    if image.background_only:

        image.hard_reject = True
        image.keep_image = False

        image.decision_reason = "Background only"

        image.decision_log.append("Background")

        return image

    ###################################################
    # Very Small Crop
    ###################################################

    if image.page_ratio < 0.01:

        image.hard_reject = True
        image.keep_image = False

        image.decision_reason = "Tiny crop"

        image.decision_log.append("Tiny")

        return image

    ###################################################
    # Too Much OCR Text
    ###################################################

    if image.word_count > 120:

        image.hard_reject = True
        image.keep_image = False

        image.decision_reason = "Paragraph image"

        image.decision_log.append("Paragraph")

        return image

    ###################################################
    # Florence Decision
    ###################################################

    if image.semantic_decision == "REMOVE":

        image.hard_reject = True
        image.keep_image = False

        image.decision_reason = "Florence removed"

        image.decision_log.append("Semantic REMOVE")

        return image

    ###################################################
    # Caption Keywords
    ###################################################

    caption = image.florence_caption.lower()

    for word in REMOVE_WORDS:

        if word in caption:

            image.hard_reject = True

            image.keep_image = False

            image.decision_reason = f"Caption contains '{word}'"

            image.decision_log.append(word)

            return image

    ###################################################
    # High Context
    ###################################################

    if image.context_score >= 20:

        image.keep_image = True

        image.decision_log.append("High Context")

    ###################################################
    # Caption Keep Words
    ###################################################

    for word in KEEP_WORDS:

        if word in caption:

            image.keep_image = True

            image.decision_log.append(word)

            break

    ###################################################
    # Layout
    ###################################################

    if image.layout_type in {

        "diagram",
        "table",
        "chart",
        "graph"

    }:

        image.keep_image = True

        image.decision_log.append(image.layout_type)

    ###################################################
    # Finished
    ###################################################

    if image.keep_image:

        image.decision_reason = "Passed hard rules"

    return image


# --------------------------------------------------
# Entire Dataset
# --------------------------------------------------

def apply_hard_rules(images):

    print("\n==============================")
    print("STAGE 7.2 : HARD RULES")
    print("==============================")

    keep = 0

    reject = 0

    for image in images:

        apply_rules(image)

        if image.keep_image:

            keep += 1

        else:

            reject += 1

    print(f"Images : {len(images)}")
    print(f"KEEP    : {keep}")
    print(f"REJECT  : {reject}")

    print("\nSample\n")

    for image in images[:10]:

        print(

            f"Page {image.page_no:3} | "

            f"Keep={image.keep_image} | "

            f"Reason={image.decision_reason}"

        )

    return images