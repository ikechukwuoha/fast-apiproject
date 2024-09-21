from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, List
from app.internal.adminServices.authorization_services.permisions_services import create_permission, get_permission_by_id, get_permission_by_name, update_permission, delete_permission
from app.internal.authorization.models.permisions import Permission
from app.utils.generic_crud import get_name_and_id
from app.database.db import permissions_collection

router = APIRouter()

# Create a permission
@router.post("/permissions", response_model=Permission)
async def create_permission_route(permission_data: Permission):
    return await create_permission(permission_data)

# Get a permission by ID
@router.get("/permissions/{permission_id}", response_model=Permission)
async def get_permission_route(permission_id: str):
    permission = await get_permission_by_id(permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission


# Get a permission by name
@router.get("/permission/name/{name}", response_model=Permission)
async def get_permission_by_name_route(name: str):
    permission = await get_permission_by_name(name)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission


# Get permissions
@router.get("/permissions", response_model=List[Dict[str, str]])
async def get_permissions():
    return await get_name_and_id(permissions_collection)




# Update a permission
@router.put("/permissions/{permission_id}", response_model=bool)
async def update_permission_route(permission_id: str, update_data: Dict[str, Any]):
    return await update_permission(permission_id, update_data)



# Delete a permission
@router.delete("/permissions/{permission_id}", response_model=bool)
async def delete_permission_route(permission_id: str):
    return await delete_permission(permission_id)
