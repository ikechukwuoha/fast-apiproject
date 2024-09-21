from pymongo.errors import PyMongoError
from bson import ObjectId
import re
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from typing import Dict, Any, List, Union
from app.database.db import groups_collection, permissions_collection
from app.internal.adminServices.authorization_services.group_services import add_permissions_to_group, add_user_to_group, create_group, get_group_by_id, get_group_by_name, get_permissions_data, get_user_data, remove_permission_from_group, remove_user_from_group, update_group, delete_group
from app.internal.authorization.models.groups import Group
from app.internal.authorization.schemas.group_schema import GroupCreate, GroupResponse
from app.internal.authorization.schemas.permissions_schema import PermissionBase
from app.utils.generic_crud import create_item, get_name_and_id
from app.database.db import users_collection

router = APIRouter()

# Create a group
@router.post("/groups", response_model=Group)
async def create_group_route(group_data: GroupCreate):
    try:
        return await create_item(groups_collection, group_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

# Get a group by ID
@router.get("/groups/{group_id}", response_model=Group)
async def create_group_route(group_data: GroupCreate):
    try:
        created_group = await create_item(groups_collection, group_data)
        # Create the response model instance
        return GroupResponse(name=created_group.name, description=created_group.description)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

# Get a group by name
@router.get("/groups/name/{name}", response_model=Group)
async def get_group_by_name_route(name: str):
    group = await get_group_by_name(name)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group


# Get groups
@router.get("/groups", response_model=List[Dict[str, str]])
async def get_groups():
    return await get_name_and_id(groups_collection)


# Update a group
@router.put("/groups/{group_id}", response_model=bool)
async def update_group_route(group_id: str, update_data: Dict[str, Any]):
    return await update_group(group_id, update_data)

# Delete a group
@router.delete("/groups/{group_id}", response_model=bool)
async def delete_group_route(group_id: str):
    return await delete_group(group_id)

    



@router.post("/groups/{group_id}/users/{identifier}")
async def add_user_to_group_by_identifier(
    group_id: str = Path(..., description="The ID of the group"),
    identifier: str = Path(..., description="The ID or email of the user")
):
    try:
        # Validate ObjectId format
        if not ObjectId.is_valid(group_id):
            raise HTTPException(status_code=400, detail="Invalid group ID format")
        
        # Convert group_id to ObjectId
        group_id = ObjectId(group_id)

        # Fetch user data by either ID or email
        user_data = await get_user_data(identifier)
        
        # Add the user to the group
        await add_user_to_group(groups_collection, group_id, user_data)

        return {"message": "User added to the group successfully."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException as e:
        raise e
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail="An internal database error occurred.")
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Log the exception during development
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {str(e)}")




@router.delete("/groups/{group_id}/users/{identifier}")
async def remove_user_from_group_endpoint(
    group_id: str = Path(..., description="The ID of the group"),
    identifier: str = Path(..., description="The ID or email of the user")
):
    try:
        # Validate group_id format and convert to ObjectId
        if not ObjectId.is_valid(group_id):
            raise HTTPException(status_code=400, detail="Invalid group ID format.")
        
        group_id = ObjectId(group_id)

        # Fetch user data (by user_id or email)
        user_data = await get_user_data(identifier)
        user_id = user_data["user_id"]  # Extract the user_id from the data
        
        # Remove the user from the group
        await remove_user_from_group(groups_collection, group_id, user_id)

        return {"message": "User removed from the group successfully."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException as e:
        raise e
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail="An internal database error occurred.")
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Log the exception during development
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {str(e)}")


    
    
    
@router.post("/groups/{group_id}/permissions/{identifier}", response_model=None)
async def add_permission_to_group_by_identifier(
    group_id: str = Path(..., description="The ID of the group"),
    identifier: str = Path(..., description="The ID or permission name")
):
    try:
        # Validate ObjectId format
        if not ObjectId.is_valid(group_id):
            raise HTTPException(status_code=400, detail="Invalid group ID format")
        
        # Convert group_id to ObjectId
        group_id = ObjectId(group_id)

        # Fetch user data by either ID or email
        permissions_data = await get_permissions_data(identifier)
        
        # Add the user to the group
        await add_permissions_to_group(groups_collection, group_id, permissions_data)

        return {"message": "Permission added to the group successfully."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException as e:
        raise e
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail="An internal database error occurred.")
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Log the exception during development
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {str(e)}")




@router.delete("/groups/{group_id}/permissions/{identifier}")
async def remove_permission_from_group_endpoint(
    group_id: str = Path(..., description="The ID of the group"),
    identifier: str = Path(..., description="The ID of the permission")
):
    try:
        # Validate group_id format and convert to ObjectId
        if not ObjectId.is_valid(group_id):
            raise HTTPException(status_code=400, detail="Invalid group ID format.")
        
        group_id = ObjectId(group_id)

        # Remove the permission from the group
        await remove_permission_from_group(groups_collection, group_id, identifier)

        return {"message": "Permission removed from the group successfully."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException as e:
        raise e
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail="An internal database error occurred.")
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Log the exception during development
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {str(e)}")



