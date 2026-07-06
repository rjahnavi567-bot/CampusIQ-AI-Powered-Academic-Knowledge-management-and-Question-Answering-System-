from app.services.image_v2.layout_detector import detect_figures

figures = detect_figures(

    "data mining Book.pdf",

    "layout_output"

)

print()

print("Detected",len(figures),"figures")

for f in figures:

    print(f)