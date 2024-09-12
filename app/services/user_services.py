from pymongo import MongoClient
from bson import ObjectId
from typing import Optional
from app.schemas.users import User, UserInDB, UserCreate, UserResponse
from app.utils.security import hash_password, verify_password
from app.config.settings import settings
from datetime import datetime

client = MongoClient(settings.MONGO_URI)
db = client[settings.DATABASE_NAME]
users_collection = db["users"]

def get_user_by_email(email: str) -> Optional[UserInDB]:
    user = users_collection.find_one({"email": email})
    if user:
        return UserInDB(**user)
    return None

def create_user(user_data: UserCreate) -> UserResponse:
    hashed_password = hash_password(user_data.password)
    user_dict = {
        "first_name": user_data.first_name,
        "other_name": user_data.other_name,
        "last_name": user_data.last_name,
        "phone": user_data.phone,
        "email": user_data.email,
        "disabled": True,
        "hashed_password": hashed_password,
        "created_at": datetime.now(),
        "updated_at": datetime.now()    
    }
    
    inserted_id = users_collection.insert_one(user_dict).inserted_id
    user_dict["_id"] = str(inserted_id)

    user_response = UserResponse(**user_dict)
    return user_response



def authenticate_user(email: str, password: str) -> Optional[User]:
    user = users_collection.find_one({"email": email})
    if user and verify_password(password, user["hashed_password"]):
        return user
    return None
