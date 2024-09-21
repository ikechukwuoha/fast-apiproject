import json
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from app.config.settings import settings
from app.internal.adminSchema.admin_user import AdminUserCreate, AdminUserResponse, AdminLoginRequest, AdminUserUpdate
from app.internal.adminServices.adminUser import register_admin_user, authenticate_admin_user, login_admin_user_service, update_admin_user
from app.utils.security import create_access_token
from datetime import timedelta
from pydantic import BaseModel

router = APIRouter()




# This is The Sign-Up Route
@router.post("/register_admin", response_model=AdminUserResponse)
async def register_user_endpoint(user_data: AdminUserCreate):
    return await register_admin_user(user_data)
 




# Sign In Route
@router.post("/login_admin")
async def admin_login_user_endpoint(request: AdminLoginRequest):
    # Use the service layer function to handle user login and get the response
    return await login_admin_user_service(request)



# Update Route
@router.put("/update_admin_user/{user_id}", response_model=AdminUserResponse)
async def update_user_endpoint(
    user_id: str,
    user_data: AdminUserUpdate
):
    """Update user information."""
    updated_user = await update_admin_user(user_id, user_data)
    return updated_user
