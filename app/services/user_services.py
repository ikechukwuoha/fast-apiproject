# app/services/user_service.py
from typing import Optional
from bson import ObjectId
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from app.config.settings import settings
from app.schemas.users import User, UserInDB, UserCreate, UserResponse, LoginRequest
from app.utils.security import create_access_token, hash_password, verify_password
from app.database.db import users_collection

async def get_user_by_email(email: str) -> Optional[UserInDB]:
    """Retrieve a user by email asynchronously."""
    user = await users_collection.find_one({"email": email})
    if user:
        return UserInDB(**user)
    return None

async def create_user(user_data: UserCreate) -> UserResponse:
    """Create a new user with the provided data asynchronously."""
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
    
    result = await users_collection.insert_one(user_dict)
    user_dict["_id"] = str(result.inserted_id)

    user_response = UserResponse(**user_dict)
    return user_response



async def register_user(user_data: UserCreate) -> UserResponse:
    """Check for existing user and create a new user if none exists."""
    # Check if the user already exists by email
    existing_user = await get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # If the user does not exist, create a new one
    new_user = await create_user(user_data)
    return new_user



async def authenticate_user(email: str, password: str) -> Optional[User]:
    """Authenticate a user by email and password asynchronously."""
    user = await users_collection.find_one({"email": email})
    if user and verify_password(password, user["hashed_password"]):
        return User(**user)
    return None


async def login_user_service(request: LoginRequest) -> JSONResponse:
    """Handle user login by validating credentials and generating a response with an access token."""
    # Authenticate the user
    user = await authenticate_user(request.email, request.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Set access token expiration
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Generate the access token
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    
    # Prepare the response
    response = JSONResponse(
        content={"access_token": access_token, "token_type": "bearer"}
    )
    
    # Set HTTP-only cookie with access token
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="Strict",
        expires=access_token_expires.total_seconds()
    )
    
    return response