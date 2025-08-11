from pydantic import BaseModel, Field
from typing import List, Optional

class FoodCreate(BaseModel):
    name: str
    description: Optional[str]
    price: float
    tags: List[str] = []

class FoodOut(FoodCreate):
    id: str
    owner_id: str