def merge_boxes(pp_boxes, doc_boxes):

    merged = []

    merged.extend(pp_boxes)
    merged.extend(doc_boxes)

    return merged