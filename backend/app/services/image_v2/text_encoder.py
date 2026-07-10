import torch

from .clip_model import (
    MODEL,
    TOKENIZER,
    DEVICE
)

# --------------------------------------------------
# Vision Categories
# --------------------------------------------------

PROMPTS = {

    "diagram": [

        "an engineering diagram",
        "a computer science diagram",
        "a software architecture diagram",
        "a block diagram",
        "a workflow diagram",
        "a labeled diagram",
        "a textbook illustration",
        "a textbook figure"

    ],

    "flowchart": [

        "a process flowchart"

    ],

    "graph": [

        "a line graph",
        "a scatter plot",
        "a histogram"

    ],

    "chart": [

        "a pie chart",
        "a bar chart"

    ],

    "table": [

        "a data table",
        "a comparison table"

    ],

    "equation": [

        "a mathematical equation",
        "a formula sheet"

    ],

    "photo": [

        "a real world photograph",
        "a laboratory photograph",
        "an equipment photograph"

    ],

    "chemical": [

        "a chemistry diagram",
        "a chemical structure"

    ],

    "medical": [

        "a microscope image",
        "a medical illustration"

    ],

    "paragraph": [

        "a paragraph of text",
        "a page full of text"

    ],

    "heading": [

        "a heading"

    ],

    "logo": [

        "a company logo"

    ],

    "icon": [

        "a decorative icon"

    ],

    "watermark": [

        "a watermark"

    ],

    "handwritten": [

        "a handwritten note"

    ],

    "screenshot": [

        "a software screenshot"

    ]
}

# --------------------------------------------------
# Encode Prompts
# --------------------------------------------------
def encode_prompts():

    print("\n==============================")
    print("TEXT ENCODER")
    print("==============================")

    category_embeddings = {}

    total_prompts = 0

    for category, prompt_list in PROMPTS.items():

        tokens = TOKENIZER(prompt_list).to(DEVICE)

        with torch.no_grad():

            features = MODEL.encode_text(tokens)

        features = features / features.norm(
            dim=-1,
            keepdim=True
        )

        category_embeddings[category] = features.cpu()

        total_prompts += len(prompt_list)

    print()
    print(f"Encoded {total_prompts} prompts")
    print(f"Categories : {len(category_embeddings)}")

    return category_embeddings