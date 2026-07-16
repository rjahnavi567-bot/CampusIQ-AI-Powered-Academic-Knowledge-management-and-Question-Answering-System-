def adaptive_expand(box, image_shape):

    height, width = image_shape[:2]

    x1, y1, x2, y2 = box

    box_w = x2 - x1
    box_h = y2 - y1

    # Expand by 6% of box size
    expand_x = max(20, int(box_w * 0.08))
    expand_y = max(20, int(box_h * 0.08))

    x1 -= expand_x
    y1 -= expand_y

    x2 += expand_x
    y2 += expand_y

    x1 = max(0, x1)
    y1 = max(0, y1)

    x2 = min(width, x2)
    y2 = min(height, y2)

    return (x1, y1, x2, y2)