from typing import List
from enum import Enum
from pydantic import BaseModel

class AnswerEnum(str, Enum):
    yes = "yes"
    no = "no"

class Answer(BaseModel):
    value: AnswerEnum

class Question(BaseModel):
    text: str
    answers: List[Answer]

class QuestionDB(Question):
    id: str

class Section(BaseModel):
    name: str
    description: str
    questions: List[Question] = []
    questions_ids: List[str] = []  # Corrected attribute name

class SectionDB(Section):
    id: str

class IndustrialCategory(BaseModel):
    name: str
    description: str
    sections: List[Section] = []

    class Config:
        schema_extra = {
            "example": {
                "name": "Example Industrial Category",
                "description": "This is an example industrial category",
                "sections": [
                    {
                        "name": "Section 1",
                        "description": "This is the first section",
                        "questions": [
                            {
                                "text": "Question 1 in Section 1",
                                "answers": [{"value": "yes"}, {"value": "no"}]
                            },
                            {
                                "text": "Question 2 in Section 1",
                                "answers": [{"value": "yes"}, {"value": "no"}]
                            }
                        ]
                    },
                    {
                        "name": "Section 2",
                        "description": "This is the second section",
                        "questions": [
                            {
                                "text": "Question 1 in Section 2",
                                "answers": [{"value": "yes"}, {"value": "no"}]
                            },
                            {
                                "text": "Question 2 in Section 2",
                                "answers": [{"value": "yes"}, {"value": "no"}]
                            }
                        ]
                    }
                ]
            }
        }

class IndustrialCategoryDB(IndustrialCategory):
    id: str
