import re


# Keywords commonly used in academic books
KEYWORDS = [
    "figure",
    "fig",
    "diagram",
    "table",
    "chart",
    "graph",
    "algorithm",
    "architecture",
    "flowchart",
    "block diagram"
]


def clean_title(title: str):

    title = title.strip()

    title = re.sub(r"\s+", " ", title)

    title = re.sub(
        r"^(figure|fig|table|chart|graph|algorithm)\.?\s*\d+(\.\d+)*[:\-]?\s*",
        "",
        title,
        flags=re.I
    )

    return title.strip()


def extract_figure_title(page_text: str):

    """
    Returns:

    title
    confidence

    """

    if not page_text:

        return None, 0.0

    lines = [

        line.strip()

        for line in page_text.splitlines()

        if line.strip()

    ]

    # --------------------------------------------------
    # Pass 1
    # Figure 4.2 CPU Organization
    # --------------------------------------------------

    pattern = re.compile(

        r"^(figure|fig|table|chart|graph|algorithm)\.?\s*\d+(\.\d+)*[:\-]?\s*(.+)$",

        re.I

    )

    for line in lines:

        match = pattern.match(line)

        if match:

            title = clean_title(match.group(0))

            if len(title) > 3:

                return title, 0.95

    # --------------------------------------------------
    # Pass 2
    # Figure 4.2
    # CPU Organization
    # --------------------------------------------------

    for i, line in enumerate(lines[:-1]):

        if re.match(

            r"^(figure|fig|table|chart|graph|algorithm)\.?\s*\d+(\.\d+)*$",

            line,

            re.I

        ):

            next_line = clean_title(lines[i + 1])

            if len(next_line) > 3:

                return next_line, 0.90

    # --------------------------------------------------
    # Pass 3
    # Block Diagram of Computer System
    # Memory Hierarchy
    # Bus Architecture
    # --------------------------------------------------

    for line in lines:

        lower = line.lower()

        if any(word in lower for word in KEYWORDS):

            if len(line) > 4:

                return clean_title(line), 0.80

    return None, 0.0