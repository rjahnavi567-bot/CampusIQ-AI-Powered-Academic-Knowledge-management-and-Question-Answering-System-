import requests

BASE_URL = "http://127.0.0.1:8000"

with open(
    "evaluation/questions.txt",
    "r",
    encoding="utf-8"
) as f:

    questions = [
        q.strip()
        for q in f.readlines()
        if q.strip()
    ]

for question in questions:

    response = requests.get(
        f"{BASE_URL}/search",
        params={
            "query": question
        }
    )

    data = response.json()

    print("\n")
    print("=" * 80)

    print("QUESTION:")
    print(question)

    print("\nTOP RESULTS:\n")

    for i, result in enumerate(
        data["results"],
        start=1
    ):

        print(f"Result {i}")

        print(
            "Topic:",
            result.get("topic", "")
        )

        print(
            result["content"][:300]
        )

        print("\n")