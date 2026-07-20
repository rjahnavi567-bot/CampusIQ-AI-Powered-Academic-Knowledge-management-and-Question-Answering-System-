from app.services.image_v2.hybrid.hybrid_extractor import HybridExtractor

extractor = HybridExtractor()

results = extractor.process_document(

    "unit.pdf"

)

print()

print("======================")

print("Pages:", len(results))

total = sum(len(p["regions"]) for p in results)

print("Total Regions:", total)

print("======================")