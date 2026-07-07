from app.services.image_v2.page_renderer import render_pdf
from app.services.image_v2.layout_detector import detect_figures
from app.services.image_v2.region_detector import detect_regions
from app.services.image_v2.region_fusion import fuse_regions

pages = render_pdf("uploads/data mining Book.pdf")

page = pages[0]

layout = detect_figures(
    page["image"]
)

regions = detect_regions(
    page["image"]
)

final = fuse_regions(
    layout,
    regions
)

print("PPStructure :", len(layout))
print("Regions     :", len(regions))
print("Final       :", len(final))