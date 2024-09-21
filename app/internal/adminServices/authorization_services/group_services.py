from typing import Dict, List,  Union, Any
from app.database.db import users_collection
from fastapi import HTTPException
from app.database.db import groups_collection, permissions_collection
from app.internal.authorization.models.groups import Group
from app.internal.authorization.schemas.permissions_schema import PermissionBase
from app.utils.generic_crud import assign_permissions, create_item, get_item_by_id, get_item_by_name, update_item, delete_item
from pymongo import UpdateOne
from pymongo.errors import PyMongoError
from typing import Dict, Any
from bson import ObjectId


""" A FUNCTION THAT CRUD GROUPS """

# Create a group
async def create_group(group_data: Group) -> Group:
    return await create_item(groups_collection, group_data)

# Get a group by ID
async def get_group_by_id(group_id: str) -> Group:
    return await get_item_by_id(groups_collection, group_id, Group)

# Get a group by name
async def get_group_by_name(name: str) -> Group:
    return await get_item_by_name(groups_collection, name, Group)

# Assign permissions to a role using the generic assign_permissions
async def assign_permissions_to_role(role_id: str, permissions: List[str]):
    await assign_permissions(groups_collection, role_id, permissions)

# Update a group
async def update_group(group_id: str, update_data: Dict[str, any]) -> bool:
    return await update_item(groups_collection, group_id, update_data)

# Delete a group
async def delete_group(group_id: str) -> bool:
    return await delete_item(groups_collection, group_id)


"""A FUNCTION TO ADD USERS TO GROUP"""

async def add_user_to_group(collection, group_id: str, user_id: str, user_data: Dict[str, Any]) -> None:
    try:
        result = await collection.update_one(
            {"_id": ObjectId(group_id)},  # Match group by _id
            {"$set": {f"users.{user_id}": user_data}}  # Add or update user in the `users` field
        )
        if result.matched_count == 0:
            raise ValueError("Group not found.")
        if result.modified_count == 0:
            raise ValueError("User could not be added.")
    except PyMongoError as e:
        raise ValueError(f"An error occurred while adding user to the group: {e}")


"""THIS FUNCTION GETS USER DATA"""    
# Define the function to get user data by either ID or email
async def get_user_data(identifier: str) -> Dict[str, Any]:
    # Check if the identifier is a valid ObjectId (i.e., user_id)
    if ObjectId.is_valid(identifier):
        user = await users_collection.find_one({"_id": ObjectId(identifier)})
    else:
        # Treat it as an email if not a valid ObjectId
        user = await users_collection.find_one({"email": identifier})
    
    if user is None:
        raise ValueError("User not found.")
    
    return {
        "user_id": str(user["_id"]),  # Convert ObjectId to string
        "first_name": user.get("first_name"),
        "last_name": user.get("last_name"),
        "email": user.get("email")
    }

async def add_user_to_group(
    collection, group_id: ObjectId, user_data: Dict[str, Any]
):
    user_id = user_data["user_id"]  # Get the user ID from the fetched user data
    
    # Check if the user is already in the group
    group = await collection.find_one({"_id": group_id})
    if group and user_id in group.get("users", {}):
        raise HTTPException(status_code=400, detail="User already in the group.")
    
    # Update the group with the new user
    result = await collection.update_one(
        {"_id": group_id},
        {"$set": {f"users.{user_id}": user_data}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Group not found.")
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Failed to add user to the group.")
    
    

# Define the function to remove a user from a group
async def remove_user_from_group(
    collection, group_id: ObjectId, user_id: str
):
    # Check if the user exists in the group
    group = await collection.find_one({"_id": group_id})
    
    if not group:
        raise HTTPException(status_code=404, detail="Group not found.")
    
    if user_id not in group.get("users", {}):
        raise HTTPException(status_code=404, detail="User not found in the group.")
    
    # Update the group by removing the user
    result = await collection.update_one(
        {"_id": group_id},
        {"$unset": {f"users.{user_id}": ""}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Failed to remove user from the group.")






# Define the function to get Permission data by either ID or email
async def get_permissions_data(identifier: str) -> Dict[str, Any]:
    # Check if the identifier is a valid ObjectId (i.e., user_id)
    if ObjectId.is_valid(identifier):
        permissions = await permissions_collection.find_one({"_id": ObjectId(identifier)})
    else:
        # Treat it as an email if not a valid ObjectId
        permissions = await permissions_collection.find_one({"name": identifier})
    
    if permissions is None:
        raise ValueError("Permission not found.")
    
    return {
        "permissions_id": str(permissions["_id"]),  # Convert ObjectId to string
        "name": permissions.get("name"),
        "description": permissions.get("description"),
    }
    

async def add_permissions_to_group(
    collection, group_id: ObjectId, permissions_data: Dict[str, Any]
):
    permissions_id = permissions_data["permissions_id"]  # Get the permission ID from the fetched user data
    
    # Check if the user is already in the group
    group = await collection.find_one({"_id": group_id})
    if group and permissions_id in group.get("users", {}):
        raise HTTPException(status_code=400, detail="Permission already in the group.")
    
    # Update the group with the new user
    result = await collection.update_one(
        {"_id": group_id},
        {"$set": {f"permissions.{permissions_id}": permissions_data}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Group not found.")
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Failed to add user to the group.")
    
    

# Define the function to remove a permission from a group
async def remove_permission_from_group(
    collection, group_id: ObjectId, permission_id: str
):
    # Check if the group exists
    group = await collection.find_one({"_id": group_id})
    
    if not group:
        raise HTTPException(status_code=404, detail="Group not found.")
    
    # Check if the permission exists in the group's permissions object
    if permission_id not in group.get("permissions", {}):
        raise HTTPException(status_code=404, detail="Permission not found in the group.")
    
    # Remove the permission by using $unset
    result = await collection.update_one(
        {"_id": group_id},
        {"$unset": {f"permissions.{permission_id}": ""}}  # Unset the permission from the object
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Failed to remove permission from the group.")
    
    return {"message": "Permission removed from the group successfully."}

