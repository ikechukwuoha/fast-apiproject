from typing import Dict
from app.database.db import permissions_collection
from app.internal.authorization.models.permisions import Permission
from app.utils.generic_crud import create_item, get_item_by_id, get_item_by_name, update_item, delete_item

# Create a permission
async def create_permission(permission_data: Permission) -> Permission:
    return await create_item(permissions_collection, permission_data)

# Get a permission by ID
async def get_permission_by_id(permission_id: str) -> Permission:
    return await get_item_by_id(permissions_collection, permission_id, Permission)

# Get a permission by name
async def get_permission_by_name(name: str) -> Permission:
    return await get_item_by_name(permissions_collection, name, Permission)

# Update a permission
async def update_permission(permission_id: str, update_data: Dict[str, any]) -> bool:
    return await update_item(permissions_collection, permission_id, update_data)

# Delete a permission
async def delete_permission(permission_id: str) -> bool:
    return await delete_item(permissions_collection, permission_id)
