import os

from app.services.image_v2.caption_generator import (
    generate_caption
)

folder = "layout_output"

for file in os.listdir(folder)[:10]:

    path = os.path.join(folder, file)

    print(file)

    print(generate_caption(path))

    print("-" * 60)