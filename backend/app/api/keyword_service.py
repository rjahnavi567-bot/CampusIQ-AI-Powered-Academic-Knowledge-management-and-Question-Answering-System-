import yake

def extract_keywords(text):

    extractor = yake.KeywordExtractor(
        lan="en",
        n=2,
        top=5
    )

    keywords = extractor.extract_keywords(text)

    return [kw[0] for kw in keywords]

