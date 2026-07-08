import torch

from .clip_model import (
    MODEL,
    TOKENIZER,
    DEVICE
)

# --------------------------------------------------
# Vision Categories
# --------------------------------------------------

PROMPTS = [

    "a diagram",

    "a flowchart",

    "a graph",

    "a chart",

    "a table",

    "a photograph",

    "a person",

    "a logo",

    "an icon",

    "a paragraph of text",

    "a page full of text",

    "a handwritten note",

    "a screenshot",

    "a microscope image",

    "a medical image",

    "a chemical structure",

    "a mathematical equation"

]

# --------------------------------------------------
# Encode Prompts
# --------------------------------------------------

def encode_prompts():

    print("\n==============================")
    print("TEXT ENCODER")
    print("==============================")

    tokens = TOKENIZER(PROMPTS)

    tokens = tokens.to(DEVICE)

    with torch.no_grad():

        features = MODEL.encode_text(tokens)

    features = features / features.norm(
        dim=-1,
        keepdim=True
    )

    prompt_embeddings = {}

    for prompt, embedding in zip(PROMPTS, features):

        prompt_embeddings[prompt] = embedding.cpu()

    print()

    print(f"Encoded {len(prompt_embeddings)} prompts")

    return prompt_embeddings