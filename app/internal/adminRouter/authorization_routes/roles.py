from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, List
from app.internal.adminServices.authorization_services.role_services import create_role, get_role_by_id, get_role_by_name, update_role, delete_role
from app.internal.authorization.models.roles import Role
from app.utils.generic_crud import get_name_and_id
from app.database.db import roles_collection

router = APIRouter()

# Create a role
@router.post("/roles", response_model=Role)
async def create_role_route(role_data: Role):
    return await create_role(role_data)

# Get a role by ID
@router.get("/roles/{role_id}", response_model=Role)
async def get_role_route(role_id: str):
    role = await get_role_by_id(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


# Get a role by name
@router.get("/role/name/{name}", response_model=Role)
async def get_role_by_name_route(name: str):
    role = await get_role_by_name(name)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


# Get roles
@router.get("/roles", response_model=List[Dict[str, str]])
async def get_roles():
    return await get_name_and_id(roles_collection)



# Update a role
@router.put("/roles/{role_id}", response_model=bool)
async def update_role_route(role_id: str, update_data: Dict[str, Any]):
    role = await get_role_by_id(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return await update_role(role_id, update_data)



# Delete a role
@router.delete("/roles/{role_id}", response_model=bool)
async def delete_role_route(role_id: str):
    role = await get_role_by_id(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return await delete_role(role_id)




