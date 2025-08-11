# src/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException
from src.db.db import get_database
import bcrypt

router = APIRouter()

@router.post("/signup")
async def signup(username:str,email:str,password:str,role:str,db=Depends(get_database)):
    users_collection = db["users"]

    if await users_collection.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    await users_collection.insert_one({
        "username": username,
        "email": email,
        "password": hashed_pw.decode("utf-8"),
        "role": "user"
    })
    return {"message": "User created"}
@router.post("/login")
async def login(email: str, password: str, db=Depends(get_database)):
    users_collection = db["users"]
    user = await users_collection.find_one({"email": email})
    if not user or not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"message": "Login successful"}
