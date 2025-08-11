# src/db/db.py
from motor.motor_asyncio import AsyncIOMotorClient
from src.config.config import settings

client = None
db = None

async def get_database():
    global client, db
    if not client:
        client = AsyncIOMotorClient(settings.MONGO_URI)
        db = client[settings.DB_NAME]
        print(f"✅ Connected to MongoDB: {settings.DB_NAME}")
    return db
