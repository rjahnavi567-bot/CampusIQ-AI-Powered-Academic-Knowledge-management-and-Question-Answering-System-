def extract_keywords(text):

    words = text.split()

    keywords = []

    for word in words:

        word = word.strip(",.()[]{}")

        if len(word) > 5:

            keywords.append(word.lower())

    unique_keywords = list(set(keywords))

    return unique_keywords[:10]