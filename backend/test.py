from app.services.image_v2.hybrid.hybrid_extractor import HybridExtractor

extractor = HybridExtractor()

regions = extractor.process_image(
    "page_156.png"
)

print()

print("="*60)

print("Detected Regions")

print("="*60)

for r in regions:

    print(r)