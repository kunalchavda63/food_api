from datetime import datetime
from bson import ObjectId

def user_document(name: str, email: str, hashed_password: str, role: str = "user"):
    return {
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
