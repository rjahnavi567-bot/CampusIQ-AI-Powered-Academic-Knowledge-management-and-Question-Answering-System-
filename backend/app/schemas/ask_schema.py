from pydantic import BaseModel
from typing import List


class AskRequest(BaseModel):

    question: str

    marks: int

    documents: List[str] = []