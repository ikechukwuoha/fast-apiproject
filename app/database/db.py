# database/db.py
from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings

# Create a Motor client and connect to the MongoDB database
client = AsyncIOMotorClient(settings.MONGO_URI)
database = client[settings.DATABASE_NAME]

# Access the users collection
users_collection = database["users"]
