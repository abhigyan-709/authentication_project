# models/user_response.py
from typing import List
from pydantic import BaseModel

class UserResponseAnswer(BaseModel):
    question_id: str
    question_text: str
    answer: str

class UserResponseSection(BaseModel):
    section_id: str
    section_name: str
    answers: List[UserResponseAnswer]

class UserResponse(BaseModel):
    user_id: str
    industrial_category_id: str
    industry_name: str
    sections: List[UserResponseSection]
