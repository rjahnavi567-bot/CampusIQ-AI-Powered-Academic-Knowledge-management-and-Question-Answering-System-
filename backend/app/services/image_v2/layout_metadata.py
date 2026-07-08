import cv2

from .layout_structure_analyzer import (
    white_ratio,
    black_ratio,
    edge_density,
    connected_components,
    contour_count,
    horizontal_lines,
    vertical_lines,
    line_density,
    diagram_score,
    table_score,
    chart_score,
    photo_score,
)


def analyze_layout(images):

    print("\n==============================")
    print("LAYOUT STRUCTURE ANALYZER")
    print("==============================")

    for image in images:

        img = cv2.imread(image.path)

        if img is None:
            continue

        gray = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2GRAY
        )

        image.white_ratio = white_ratio(gray)

        image.black_ratio = black_ratio(gray)

        image.edge_density = edge_density(gray)

        image.connected_components = connected_components(gray)

        image.contour_count = contour_count(gray)

        image.horizontal_lines = horizontal_lines(gray)

        image.vertical_lines = vertical_lines(gray)

        image.line_density = line_density(
            image.horizontal_lines,
            image.vertical_lines
        )

        image.diagram_score = diagram_score(
            image.edge_density,
            image.connected_components
        )

        image.table_score = table_score(
            image.horizontal_lines,
            image.vertical_lines
        )

        image.chart_score = chart_score(
            image.horizontal_lines,
            image.vertical_lines,
            image.edge_density
        )

        image.photo_score = photo_score(
            image.edge_density,
            image.white_ratio
        )

        # --------------------------
        # Temporary layout label
        # --------------------------

        if image.table_score > 0.8:

            image.layout_type = "table"

        elif image.diagram_score > 0.7:

            image.layout_type = "diagram"

        elif image.chart_score > 0.7:

            image.layout_type = "chart"

        else:

            image.layout_type = "photo"

    print(f"Layout analyzed : {len(images)}")

    print("\nSample Layout Features")

    for img in images[:5]:

        print(

            f"Page {img.page_no} | "

            f"{img.layout_type:8} | "

            f"Edge={img.edge_density:.3f} | "

            f"Lines={img.line_density} | "

            f"Comp={img.connected_components}"

        )

    return images