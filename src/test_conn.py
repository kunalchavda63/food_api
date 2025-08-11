import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from urllib.parse import quote_plus

async def test():
    pwd = quote_plus("YOUR_RAW_PASSWORD")
    uri = f"mongodb+srv://kunalchavda029:{pwd}@cluster0.i75v68p.mongodb.net/food_api?retryWrites=true&w=majority"
    client = AsyncIOMotorClient(uri)
    print(await client.admin.command("ping"))
    db = client.get_database("food_api")
    print("Collections:", await db.list_collection_names())
    client.close()

asyncio.run(test())
