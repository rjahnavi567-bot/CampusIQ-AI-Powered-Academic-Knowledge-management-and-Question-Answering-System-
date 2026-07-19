from collections import Counter


def summarize(result):

    counter = Counter()

    for box in result.boxes:

        cls = result.names[int(box.cls)]

        counter[cls] += 1

    return counter