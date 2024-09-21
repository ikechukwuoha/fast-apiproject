from typing import Collection, Dict, List, Type, TypeVar
from pydantic import BaseModel
from bson import ObjectId
from pymongo import errors
from typing import Type, TypeVar
from app.database.db import permissions_collection
from app.internal.authorization.models.permisions import Permission
from fastapi import HTTPException, Depends
from jose import jwt, JWTError
from app.database.db import admin_users_collection, users_collection, groups_collection, permissions_collection, roles_collection
from app.config.settings import settings



T = TypeVar('T', bound=BaseModel)



# Create a new item
async def create_item(collection, item_data: T) -> T:
    # Check if the item already exists based on a unique field (e.g., name)
    existing_item = await collection.find_one({"name": item_data.name})
    if existing_item:
        raise ValueError("An item with this name already exists.")
    
    # Attempt to insert the item into the collection
    try:
        result = await collection.insert_one(item_data.model_dump(by_alias=True))
        # Add the inserted_id to the item data
        item_dict = item_data.model_dump()
        item_dict["id"] = str(result.inserted_id)
        return item_data.__class__(**item_dict)
    except errors.DuplicateKeyError:
        raise ValueError("An item with this name already exists.")



# Get an item by ID
async def get_item_by_id(collection, item_id: str, model: Type[T]) -> T:
    item = await collection.find_one({"_id": ObjectId(item_id)})
    return model(**item) if item else None

# Get an item by name
async def get_item_by_name(collection, name: str, model: Type[T]) -> T:
    item = await collection.find_one({"name": name})
    return model(**item) if item else None



# Assign permissions to an item (permissions will be a list of dictionaries)
async def assign_permissions(collection, item_id: str, permissions: List[Dict[str, str]], permissions_collection):
    # Validate that all permissions exist before assigning them
    permission_ids = [ObjectId(p["_id"]) for p in permissions]  # Assuming permissions contain '_id'
    existing_permissions = await permissions_collection.find({"_id": {"$in": permission_ids}}).to_list(length=len(permission_ids))

    if len(existing_permissions) != len(permissions):
        raise ValueError("One or more permissions are invalid.")
    
    # Convert each permission object to a dictionary if needed
    permissions_data = [Permission(**p).model_dump() for p in permissions]
    
    # Update the item with validated permissions
    await collection.update_one({"_id": ObjectId(item_id)}, {"$set": {"permissions": permissions_data}})



# Update an existing item
async def update_item(collection, item_id: str, update_data: Dict[str, any]) -> bool:
    result = await collection.update_one({"_id": ObjectId(item_id)}, {"$set": update_data})
    return result.modified_count > 0

# Delete an item by ID
async def delete_item(collection, item_id: str) -> bool:
    result = await collection.delete_one({"_id": ObjectId(item_id)})
    return result.deleted_count > 0




# Utility function to get only `name` and `_id`
async def get_name_and_id(collection):
    items = []
    cursor = collection.find({}, {"_id": 1, "name": 1})
    async for document in cursor:
        items.append({
            "id": str(document["_id"]),
            "name": document["name"]
        })
        print(f"Items to return: {items}")
    return items




"""This Is A Utility Function To Get The curent User Role"""
# Utility to decode JWT token
async def get_current_user(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Check if user is an admin
async def is_admin_user(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") not in ["admin", "superuser"]:
        raise HTTPException(status_code=403, detail="You do not have the required permissions")
    return current_user
