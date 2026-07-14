from app.services.image_v2.classifier import classify_image

label, score = classify_image(

    "layout_output/page_124_figure_0.png"

)

print(label)

print(score)