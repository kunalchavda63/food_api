from datetime import datetime
from typing import Optional, Dict

from bson import ObjectId
from pydantic import BaseModel


def user_document(user_id: int,name: str, email: str, hashed_password: str, role: str = "user"):
    return {
        "id": user_id,
        "name": name,
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
        "name": doc.get("name"),
        "email": doc.get("email"),
        "role": doc.get("role"),
        "onboarded": doc.get("onboarded", False),
        "profile": doc.get("profile", {}),
    }

class UserModel(BaseModel):
    id: int
    name: str
    email: str
    password: str
    role: str
    profile: Optional[Dict] = None
    onboarded: Optional[bool]

    class Config:
        orm_mode = True
