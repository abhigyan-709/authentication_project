# routes/user_response.py
from fastapi import APIRouter, Depends, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from models.user_response import UserResponse, UserResponseAnswer, UserResponseSection
from database.db import db
from routes.user import get_current_user

user_response_route = APIRouter()

# routes/user_response.py
@user_response_route.post("/user_responses/", response_model=UserResponse, tags=["User Response"])
async def create_user_response(
    user_response: UserResponse,
    current_user: str = Depends(get_current_user),
    db_client: MongoClient = Depends(db.get_client)
):
    user_response_dict = user_response.dict()

    # Perform lookups to get the names of industry, section, and question
    industrial_category_id = user_response_dict["industrial_category_id"]
    industrial_category = db_client[db.db_name]["industrial_category"].find_one(
        {"_id": ObjectId(industrial_category_id)})
    
    if industrial_category:
        user_response_dict["industry_name"] = industrial_category["name"]

        for section in user_response_dict["sections"]:
            section_id = section["section_id"]
            section_document = db_client[db.db_name]["section"].find_one(
                {"_id": ObjectId(section_id)})
            if section_document:
                section["section_name"] = section_document["name"]

                for answer in section["answers"]:
                    question_id = answer["question_id"]
                    question_document = db_client[db.db_name]["question"].find_one(
                        {"_id": ObjectId(question_id)})
                    if question_document:
                        answer["question_text"] = question_document["text"]
                    else:
                        answer["question_text"] = "Question not found"

    # Store user response in the database
    result = db_client[db.db_name]["user_response"].insert_one(user_response_dict)
    user_response_id = str(result.inserted_id)

    # Return the user response with the inserted ID
    return {**user_response_dict, "id": user_response_id}

# routes/user_response.py
@user_response_route.get("/user_responses/{user_response_id}", response_model=UserResponse, tags=["User Response"])
async def read_user_response(
    user_response_id: str,
    db_client: MongoClient = Depends(db.get_client)
):
    user_response = db_client[db.db_name]["user_response"].find_one({"_id": ObjectId(user_response_id)})
    if user_response:
        # Get industry details
        industrial_category_id = user_response["industrial_category_id"]
        industrial_category = db_client[db.db_name]["industrial_category"].find_one(
            {"_id": ObjectId(industrial_category_id)})
        industry_name = industrial_category.get("name", "Industry not found")

        # Build the response
        response = {
            "user_id": user_response["user_id"],
            "industrial_category_id": industrial_category_id,
            "industry_name": industry_name,
            "sections": []
        }

        for section in user_response.get("sections", []):
            section_id = section.get("section_id", "")
            section_name = db_client[db.db_name]["section"].find_one(
                {"_id": ObjectId(section_id)}
            ).get("name", f"Section not found for ID: {section_id}")

            response_section = {
                "section_id": section_id,
                "section_name": section_name,
                "answers": []
            }

            for answer in section.get("answers", []):
                question_id = answer.get("question_id", "")
                question_text = db_client[db.db_name]["question"].find_one(
                    {"_id": ObjectId(question_id)}
                ).get("text", f"Question not found for ID: {question_id}")

                response_answer = {
                    "question_id": question_id,
                    "question_text": question_text,
                    "answer": answer.get("answer", "")
                }

                response_section["answers"].append(response_answer)

            response["sections"].append(response_section)

        return UserResponse(**response)

    raise HTTPException(status_code=404, detail="User Response not found")
