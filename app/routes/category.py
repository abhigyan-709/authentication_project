# routes/category.py
from fastapi import APIRouter, HTTPException, Depends
from pymongo import MongoClient
from bson import ObjectId
from models.category import IndustrialCategory, IndustrialCategoryDB, Section, SectionDB, Question, QuestionDB
from database.db import db
from routes.user import get_current_user, User

industrial_route = APIRouter()

current_user: User = Depends(get_current_user)  # setting this to global variable as it's being used by many functions

def check_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Forbidden: Only admins can access this endpoint")

@industrial_route.post("/questions/", response_model=QuestionDB, tags=["Industry"])
async def create_question(
    question: Question,
    db_client: MongoClient = Depends(db.get_client),
    current_user: User = Depends(check_admin_user)  # Only admins can access this endpoint
):
    # Create the question in the database
    question_result = db_client[db.db_name]["question"].insert_one(question.dict())
    question_db = QuestionDB(**question.dict(), id=str(question_result.inserted_id))
    return question_db

@industrial_route.get("/questions/", response_model=list[QuestionDB], tags=["Question"])
async def get_questions(
    db_client: MongoClient = Depends(db.get_client),
    current_user: User = Depends(get_current_user)  # All registered users can access this endpoint
):
    # Retrieve the list of questions from the database
    questions_cursor = db_client[db.db_name]["question"].find({})
    questions = [QuestionDB(**question, id=str(question["_id"])) for question in questions_cursor]

    return questions

@industrial_route.get("/questions/{question_id}", response_model=QuestionDB, tags=["Question"])
async def get_question_by_id(
    question_id: str,
    db_client: MongoClient = Depends(db.get_client),
    current_user: User = Depends(get_current_user)  # All registered users can access this endpoint
):
    # Retrieve a question by its ID from the database
    question_doc = db_client[db.db_name]["question"].find_one({"_id": ObjectId(question_id)})
    if not question_doc:
        raise HTTPException(status_code=404, detail="Question not found")

    question_db = QuestionDB(**question_doc, id=str(question_doc["_id"]))
    return question_db

@industrial_route.put("/questions/{question_id}", response_model=QuestionDB, tags=["Question"])
async def update_question(
    question_id: str,
    updated_question: Question,
    db_client: MongoClient = Depends(db.get_client),
    current_user: User = Depends(check_admin_user)  # Only admins can access this endpoint
):
    # Update a question in the database
    updated_question_dict = updated_question.dict()
    del updated_question_dict["id"]  # Remove id from the dict to prevent update issues
    result = db_client[db.db_name]["question"].update_one({"_id": ObjectId(question_id)}, {"$set": updated_question_dict})

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Question not found")

    updated_question_db = QuestionDB(**updated_question_dict, id=question_id)
    return updated_question_db

@industrial_route.delete("/questions/{question_id}", response_model=QuestionDB, tags=["Question"])
async def delete_question(
    question_id: str,
    db_client: MongoClient = Depends(db.get_client),
    current_user: User = Depends(check_admin_user)  # Only admins can access this endpoint
):
    # Delete a question from the database
    question_doc = db_client[db.db_name]["question"].find_one_and_delete({"_id": ObjectId(question_id)})
    if not question_doc:
        raise HTTPException(status_code=404, detail="Question not found")

    deleted_question_db = QuestionDB(**question_doc, id=str(question_doc["_id"]))
    return deleted_question_db

@industrial_route.post("/industrial_categories/", response_model=IndustrialCategoryDB, tags=["Industry"])
async def create_industrial_category(
    industrial_category: IndustrialCategory,
    current_user: str = Depends(get_current_user),
    db_client: MongoClient = Depends(db.get_client)
):
    # Check if the user has admin role
    check_admin_user(current_user)

    # Extract sections from the request
    sections = industrial_category.sections
    industrial_category_dict = industrial_category.dict(exclude={"sections"})

    # Create an empty list to store section IDs
    section_ids = []

    # Create sections
    for section in sections:
        # Ensure the section has questions
        questions = section.questions if section.questions else []
        # Create an empty list to store question IDs
        question_ids = []

        # Create questions
        for question in questions:
            question_result = db_client[db.db_name]["question"].insert_one(question.dict())
            question_ids.append(str(question_result.inserted_id))

        # Add question IDs to the section
        section.questions_ids = question_ids  # Corrected attribute name
        # Create the section
        section_result = db_client[db.db_name]["section"].insert_one(section.dict())
        section_ids.append(str(section_result.inserted_id))

    # Add section IDs to the industrial category
    industrial_category_dict["section_ids"] = section_ids

    # Create the industrial category
    result = db_client[db.db_name]["industrial_category"].insert_one(industrial_category_dict)
    industrial_category_db = IndustrialCategoryDB(**industrial_category.dict(), id=str(result.inserted_id))
    return industrial_category_db


@industrial_route.get("/industrial_categories/", response_model=list[IndustrialCategoryDB], tags=["Industry"])
async def get_industrial_categories(
    db_client: MongoClient = Depends(db.get_client),
    current_user: User = Depends(get_current_user)  # All registered users can access this endpoint
):
    # Retrieve the list of industrial categories from the database
    industrial_categories_cursor = db_client[db.db_name]["industrial_category"].find({})
    industrial_categories = []

    # Iterate through the cursor and convert BSON documents to models
    for industrial_category_doc in industrial_categories_cursor:
        industrial_category = IndustrialCategoryDB(**industrial_category_doc, id=str(industrial_category_doc["_id"]))
        industrial_categories.append(industrial_category)

    return industrial_categories

@industrial_route.get("/industrial_categories/{category_name}/sections", response_model=list[SectionDB], tags=["Industry"])
async def get_sections_for_category(
    category_name: str,
    db_client: MongoClient = Depends(db.get_client),
    current_user: User = Depends(get_current_user)  # All registered users can access this endpoint
):
    # Retrieve sections for the specified category from the database
    industrial_category_doc = db_client[db.db_name]["industrial_category"].find_one({"name": category_name})
    if not industrial_category_doc:
        raise HTTPException(status_code=404, detail="Category not found")

    section_ids = industrial_category_doc.get("section_ids", [])
    sections_cursor = db_client[db.db_name]["section"].find({"_id": {"$in": [ObjectId(sec_id) for sec_id in section_ids]}})
    sections = [SectionDB(**section, id=str(section["_id"])) for section in sections_cursor]

    return sections

@industrial_route.get("/sections/{section_id}/questions", response_model=list[QuestionDB], tags=["Industry"])
async def get_questions_for_section(
    section_id: str,
    db_client: MongoClient = Depends(db.get_client),
    current_user: User = Depends(get_current_user)  # All registered users can access this endpoint
):
    # Retrieve questions for the specified section from the database
    section_doc = db_client[db.db_name]["section"].find_one({"_id": ObjectId(section_id)})
    if not section_doc:
        raise HTTPException(status_code=404, detail="Section not found")

    question_ids = section_doc.get("questions_ids", [])
    questions_cursor = db_client[db.db_name]["question"].find({"_id": {"$in": [ObjectId(q_id) for q_id in question_ids]}})
    questions = [QuestionDB(**question, id=str(question["_id"])) for question in questions_cursor]

    return questions
