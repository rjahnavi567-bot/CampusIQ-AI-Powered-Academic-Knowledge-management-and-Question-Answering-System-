from app.services.image_v2.florence.florence_caption import generate_description

image = r"uploads\images\58\page_1_figure_0.png"

description = generate_description(image)

print()

print("Description")

print("----------------------")

print(description)