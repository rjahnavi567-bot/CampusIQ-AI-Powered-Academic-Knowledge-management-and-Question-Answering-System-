from collections import Counter


def print_statistics(results):

    result = results[0]

    names = result.names

    counts = Counter()

    for box in result.boxes:

        label = names[int(box.cls.item())]

        counts[label] += 1

    print("\nDetected Regions")

    print("--------------------")

    for k, v in counts.items():

        print(f"{k:<20}{v}")