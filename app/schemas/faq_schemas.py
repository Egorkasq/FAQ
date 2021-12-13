from pydantic import BaseModel
from typing import List


class FaqInfo(BaseModel):
    text_for_search: str


class FoundInfo(BaseModel):
    possible_answers: list[str]
