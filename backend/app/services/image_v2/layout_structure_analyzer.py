import cv2
import numpy as np
def white_ratio(gray):

    return float(np.mean(gray > 245))
def black_ratio(gray):

    return float(np.mean(gray < 10))
def edge_density(gray):

    edges = cv2.Canny(gray, 100, 200)

    return float(
        np.count_nonzero(edges) /
        edges.size
    )
def connected_components(gray):

    binary = cv2.adaptiveThreshold(

        gray,

        255,

        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,

        cv2.THRESH_BINARY_INV,

        25,

        15

    )

    num_labels, _, _, _ = cv2.connectedComponentsWithStats(binary)

    return int(num_labels)
def contour_count(gray):

    binary = cv2.adaptiveThreshold(

        gray,

        255,

        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,

        cv2.THRESH_BINARY_INV,

        25,

        15

    )

    contours, _ = cv2.findContours(

        binary,

        cv2.RETR_EXTERNAL,

        cv2.CHAIN_APPROX_SIMPLE

    )

    return len(contours)
def horizontal_lines(gray):

    edges = cv2.Canny(gray,50,150)

    lines = cv2.HoughLinesP(

        edges,

        1,

        np.pi/180,

        threshold=80,

        minLineLength=80,

        maxLineGap=10

    )

    if lines is None:

        return 0

    count = 0

    for line in lines:

        x1,y1,x2,y2 = line[0]

        if abs(y1-y2) < 8:

            count += 1

    return count
def vertical_lines(gray):

    edges = cv2.Canny(gray,50,150)

    lines = cv2.HoughLinesP(

        edges,

        1,

        np.pi/180,

        threshold=80,

        minLineLength=80,

        maxLineGap=10

    )

    if lines is None:

        return 0

    count = 0

    for line in lines:

        x1,y1,x2,y2 = line[0]

        if abs(x1-x2) < 8:

            count += 1

    return count
def line_density(h_lines,v_lines):

    return h_lines + v_lines
def diagram_score(edge, components):

    score = 0.0

    if edge > 0.02:

        score += 0.4

    if components > 20:

        score += 0.4

    if edge > 0.05:

        score += 0.2

    return min(score,1.0)
def table_score(h_lines,v_lines):

    score = 0.0

    if h_lines > 5:

        score += 0.5

    if v_lines > 5:

        score += 0.5

    return min(score,1.0)
def photo_score(edge,white):

    score = 1.0

    if edge > 0.05:

        score -= 0.3

    if white > 0.6:

        score -= 0.3

    return max(score,0.0)
def chart_score(h_lines,v_lines,edge):

    score = 0.0

    if h_lines >= 2:

        score += 0.3

    if v_lines >= 2:

        score += 0.3

    if edge > 0.02:

        score += 0.4

    return min(score,1.0)
