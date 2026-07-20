import os


def compare_results(old_regions, doclayout_regions):

    print("\n==============================")
    print("HYBRID COMPARISON")
    print("==============================")

    print(f"Current Pipeline : {len(old_regions)}")
    print(f"DocLayout        : {len(doclayout_regions)}")

    labels = {}

    for region in doclayout_regions:

        label = region["label"]

        labels[label] = labels.get(label, 0) + 1

    print("\nDocLayout Classes")

    for k, v in labels.items():

        print(f"{k:20} {v}")

    print("\nDifference")

    print(
        f"Extra detections = {len(doclayout_regions)-len(old_regions)}"
    )

    return {
        "old": len(old_regions),
        "doclayout": len(doclayout_regions),
        "labels": labels
    }