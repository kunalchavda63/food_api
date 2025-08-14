from datetime import datetime
from typing import Optional, Dict

from bson import ObjectId
from pydantic import BaseModel


def user_document(user_id: int,username: str, email: str, hashed_password: str, role: str = "user"):
    return {
        "id": user_id,
        "username": username,
        "email": email.lower(),
        "password": hashed_password,
        "role": role,
        "created_at": datetime.utcnow(),
        "onboarded": False,
        "profile": {},
    }

def sanitize_user(doc: dict):
    if not doc:
        return None
    return {
        "id": str(doc.get("_id")),
        "username": doc.get("username"),
        "email": doc.get("email"),
        "role": doc.get("role"),
        "onboarded": doc.get("onboarded", False),
        "profile": doc.get("profile", {}),
    }

class UserModel(BaseModel):
    id: int
    username: str
    email: str
    password: str
    role: str
    profile: Optional[Dict] = None
    onboarded: Optional[bool]

    class Config:
        orm_mode = True
