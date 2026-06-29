import re
import re

from app.services.heading_detector import is_heading
def build_sections(blocks):

    sections=[]

    current_heading="Untitled Section"

    current_text=[]

    for block in blocks:

        if block["type"]=="heading":

            if current_text:

                sections.append({
                    "heading":current_heading,
                    "text":"\n".join(current_text)
                })

            current_heading=block["text"]

            current_text=[]

        else:

            current_text.append(block["text"])

    if current_text:

        sections.append({
            "heading":current_heading,
            "text":"\n".join(current_text)
        })

    return sections

def extract_blocks(page_text: str):
    """
    Split a page into logical blocks.

    Returns:
    [
        {
            "type":"heading",
            "text":"Control Memory"
        },
        {
            "type":"paragraph",
            "text":"The control memory..."
        }
    ]
    """

    page_text = page_text.replace("\x00", "")

    lines = [
        l.strip()
        for l in page_text.splitlines()
        if l.strip()
    ]

    blocks = []

    current = []

    for line in lines:
        # heading
        if is_heading(line):

            if current:
                blocks.append({
                    "type":"paragraph",
                    "text":" ".join(current)
                })
                current=[]

            blocks.append({
                "type":"heading",
                "text":line
            })

        else:
            current.append(line)

    if current:
        blocks.append({
            "type":"paragraph",
            "text":" ".join(current)
        })

    return blocks