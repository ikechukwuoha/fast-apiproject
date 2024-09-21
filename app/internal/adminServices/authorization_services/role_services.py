from typing import Dict, List
from app.internal.authorization.models.roles import Role
from app.database.db import roles_collection
from app.utils.generic_crud import create_item, get_item_by_id, get_item_by_name, assign_permissions, update_item, delete_item


# Create a new role using generic create_item
async def create_role(role_data: Role) -> Role:
    return await create_item(roles_collection, role_data)

# Get a role by its ID using generic get_item_by_id
async def get_role_by_id(role_id: str) -> Role:
    return await get_item_by_id(roles_collection, role_id, Role)

# Get a role by its name using generic get_item_by_name
async def get_role_by_name(name: str) -> Role:
    return await get_item_by_name(roles_collection, name, Role)

# Assign permissions to a role using the generic assign_permissions
async def assign_permissions_to_role(role_id: str, permissions: List[str]):
    await assign_permissions(roles_collection, role_id, permissions)

# Update an existing role using generic update_item
async def update_role(role_id: str, update_data: Dict[str, any]) -> bool:
    return await update_item(roles_collection, role_id, update_data)

# Delete a role by ID using generic delete_item
async def delete_role(role_id: str) -> bool:
    return await delete_item(roles_collection, role_id)
