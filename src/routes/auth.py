
from typing import List
import bcrypt
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from src.db.db import get_database
from src.models.users import user_document, UserModel
from src.services.auth_service import get_next_user_id

router = APIRouter()

class SignupRequest(BaseModel):
    username: str
    email: str
    password: str
    role: str

@router.post("/signup")
async def signup(request: SignupRequest, db=Depends(get_database)):
    users_collection = db["users"]

    if await users_collection.find_one({"email": request.email}):
        raise HTTPException(status_code=400, detail="Email already exists")
    next_id = await  get_next_user_id(db)

    hashed_pw = bcrypt.hashpw(request.password.encode("utf-8"), bcrypt.gensalt())
    user_data = user_document(next_id,request.username,request.email,hashed_pw.decode("utf-8"),request.role)

    await  users_collection.insert_one(user_data)

    return {"message": "User created","user_id": next_id}


class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(request: LoginRequest, db=Depends(get_database)):
    users_collection = db["users"]
    user = await users_collection.find_one({"email": request.email})
    if not user or not bcrypt.checkpw(request.password.encode("utf-8"), user["password"].encode("utf-8")):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {
        "user_id": str(user["id"]),
        "message": "Login successful"
    }

@router.get("/all_users", response_model=List[UserModel])
async def get_all_users(
    page: int = Query(1, ge=1, description="Page number (must be >= 1)"),
    limit: int = Query(10, ge=1, le=100, description="Items per page (1-100)"),
    db=Depends(get_database)
):
    if page < 1:
        page = 1
    if limit < 1:
        limit = 1
    elif limit > 100:
        limit = 100

    skip = (page - 1) * limit
    user_collection = db["users"]

    users_list = await user_collection.find({}, {"_id": 0}) \
                                      .skip(skip) \
                                      .limit(limit) \
                                      .to_list(length=limit)

    return users_list



@router.get("/users/{user_id}", response_model=UserModel)
async def get_user_by_id(user_id: int, db=Depends(get_database)):
    users_collection = db["users"]
    user = await users_collection.find_one({"id": user_id}, {"_id": 0})  # exclude _id
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
