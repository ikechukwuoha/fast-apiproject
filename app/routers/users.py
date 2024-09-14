import json
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from app.config.settings import settings
from app.services.user_services import register_user, update_user
from app.schemas.users import UserCreate, UserResponse, LoginRequest, UserUpdate
from app.services.user_services import create_user, authenticate_user, login_user_service
from app.utils.security import create_access_token
from datetime import timedelta
from pydantic import BaseModel

router = APIRouter()




# This is The Sign-Up Route
@router.post("/register", response_model=UserResponse)
async def register_user_endpoint(user_data: UserCreate):
    return await register_user(user_data)
 




# Sign In Route
@router.post("/login")
async def login_user_endpoint(request: LoginRequest):
    # Use the service layer function to handle user login and get the response
    return await login_user_service(request)



# Update Route
@router.put("/update_user/{user_id}", response_model=UserResponse)
async def update_user_endpoint(
    user_id: str,
    user_data: UserUpdate
):
    """Update user information."""
    updated_user = await update_user(user_id, user_data)
    return updated_user
