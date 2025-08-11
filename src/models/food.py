from datetime import datetime

def food_document(name: str, description: str, price: float, tags: list[str], owner_id: str):
    return {
        "name": name,
        "description": description,
        "price": float(price),
        "tags": tags or [],
        "owner_id": owner_id,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }