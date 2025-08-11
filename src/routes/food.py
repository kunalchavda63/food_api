from fastapi import APIRouter, Depends, HTTPException
from ..schemes.food import FoodCreate
from ..app.deps import get_current_user, get_db
from ..models.food import food_document
from bson import ObjectId

router = APIRouter(prefix="/food")

@router.post("/", status_code=201)
async def create_food(payload: FoodCreate, user=Depends(get_current_user), db=Depends(get_db)):
    doc = food_document(payload.name, payload.description or "", payload.price, payload.tags, str(user.get("_id")))
    res = await db.foods.insert_one(doc)
    created = await db.foods.find_one({"_id": res.inserted_id})
    created["id"] = str(created.get("_id"))
    return created

@router.get("/")
async def list_foods(q: str = None, limit: int = 20, skip: int = 0, db=Depends(get_db)):
    filt = {}
    if q:
        filt = {"$text": {"$search": q}} if "$text" in (await db.command({"listCollections": 1})) else {"name": {"$regex": q, "$options": "i"}}
    cursor = db.foods.find(filt).skip(skip).limit(limit)
    items = []
    async for doc in cursor:
        doc["id"] = str(doc.get("_id"))
        items.append(doc)
    return {"items": items}