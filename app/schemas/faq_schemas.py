from pydantic import BaseModel
from typing import List, Optional


class FaqInfo(BaseModel):
    text_for_search: str


class FoundInfo(BaseModel):
    possible_answers: list[str] = []


class TextIndexFormat(BaseModel):
    description: str
    keyword: Optional[List[str]]



class ESInfo(BaseModel):
    question: str
    answer: TextIndexFormat


class AnswersText(BaseModel):
    answer_text: str
