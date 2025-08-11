from fastapi import APIRouter, Depends
from ..schemes.user import OnboardPayload
from ..app.deps import get_current_user, get_db
from ..models.users import sanitize_user
from bson import ObjectId

router = APIRouter(prefix="/onboard")

@router.post("/complete")
async def complete_onboarding(payload: OnboardPayload, user=Depends(get_current_user), db=Depends(get_db)):
    uid = user.get("_id")
    # allow both ObjectId and string
    try:
        uid_q = ObjectId(uid)
    except Exception:
        uid_q = uid

    await db.users.update_one({"_id": uid_q}, {"$set": {"onboarded": True, "profile": payload.dict()}})
    updated = await db.users.find_one({"_id": uid_q})
    return sanitize_user(updated)