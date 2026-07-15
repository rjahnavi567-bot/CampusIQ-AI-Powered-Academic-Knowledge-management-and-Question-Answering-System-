from dataclasses import dataclass


@dataclass
class Detection:

    bbox: tuple

    source: str

    score: float = 0.0