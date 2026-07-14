from app.services.image_v2.metadata_builder import build_metadata

sample = {

    "page_no": 124,

    "path": "page_124.png",

    "caption": "data integration diagram",

    "ocr_text": "Data cleaning Data integration",

    "category": "figure",

    "image_hash": "123"

}

meta = build_metadata(

    sample,

    "This chapter explains preprocessing and data cleaning."

)

print(meta)

print()

print(meta["search_text"])