# app/services/user_service.py
from typing import Optional
from bson import ObjectId
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from app.config.settings import settings
from app.internal.adminSchema.admin_user import AdminLoginRequest, AdminUser, AdminUserInDB, AdminUserCreate, AdminUserResponse, AdminUserUpdate
from app.utils.security import create_access_token, hash_password, verify_password
from app.database.db import admin_users_collection
from typing import Dict, Union


async def get_admin_user_by_email(email: str) -> Optional[AdminUserInDB]:
    """Retrieve a user by email asynchronously."""
    user = await admin_users_collection.find_one({"email": email})
    if user:
        return AdminUserInDB(**user)
    return None



# A Function that Stores The User In The Database
async def create_admin_user(user_data: AdminUserCreate) -> AdminUserResponse:
    """Create a new user with the provided data asynchronously."""
    hashed_password = hash_password(user_data.password)
    user_dict = {
        "first_name": user_data.first_name,
        "other_name": user_data.other_name,
        "last_name": user_data.last_name,
        "phone": user_data.phone,
        "email": user_data.email,
        "disabled": True,
        "role": user_data.role,  # Ensure this is passed
        "permission": user_data.permission, 
        "super_user": user_data.super_user,
        "hashed_password": hashed_password,
        "last_email_update": user_data.last_email_update,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    
    # Set permission to an empty dictionary if it is None
    if user_dict.get("permission") is None:
        user_dict["permission"] = {}
        
    result = await admin_users_collection.insert_one(user_dict)
    user_dict["_id"] = str(result.inserted_id)

    user_response = AdminUserResponse(**user_dict)
    return user_response


# A Function That Register The User
async def register_admin_user(user_data: AdminUserCreate) -> AdminUserResponse:
    """Check for existing user and create a new user if none exists."""
    # Check if the user already exists by email
    existing_user = await get_admin_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # If the user does not exist, create a new one
    new_user = await create_admin_user(user_data)
    return new_user



# A Function That Authenticate the User
async def authenticate_admin_user(email: str, password: str) -> Optional[AdminUser]:
    """Authenticate a user by email and password asynchronously."""
    user = await admin_users_collection.find_one({"email": email})
    if user and verify_password(password, user["hashed_password"]):
        user["id"] = str(user["_id"])
        
        return AdminUser(**user)



# A Function That Logs the User In and Generates a Token
async def login_admin_user_service(request: AdminLoginRequest) -> JSONResponse:
    """Handle user login by validating credentials and generating a response with an access token."""
    # Authenticate the user
    user = await authenticate_admin_user(request.email, request.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Set access token expiration
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Generate the access token
    access_token = create_access_token(data={"sub": user.email, "id": user.id}, expires_delta=access_token_expires)
    
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





 
"""Function For Updating A User Detail"""
async def update_admin_user(user_id: str, user_data: AdminUserUpdate) -> AdminUserResponse:
    """Update an existing user's information asynchronously."""
    user = await admin_users_collection.find_one({"_id": ObjectId(user_id)})
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    update_data = user_data.model_dump(exclude_unset=True)
    email_update_blocked = False  # Track whether the email update is blocked
    remaining_days = None  # Track remaining days for email update

    # Check if email is being updated
    if "email" in update_data:
        # Check if the user has a last email update timestamp
        if "last_email_update" in user and user["last_email_update"]:
            time_since_last_update = datetime.now() - user["last_email_update"]
            # If the last email update was less than 90 days ago, remove the email update but continue
            if time_since_last_update < timedelta(days=90):
                update_data.pop("email")  # Remove email from update
                email_update_blocked = True  # Set the flag to notify the user later
                # Calculate remaining days
                days_remaining = 90 - time_since_last_update.days
                remaining_days = days_remaining

    update_data["updated_at"] = datetime.now()

    # If email is being updated, update the last_email_update field as well
    if "email" in update_data:
        update_data["last_email_update"] = datetime.now()

    result = await admin_users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    updated_user = await admin_users_collection.find_one({"_id": ObjectId(user_id)})

    # Create UserResponse object with all required fields
    user_response = AdminUserResponse(
        first_name=updated_user["first_name"],
        other_name=updated_user["other_name"],
        last_name=updated_user["last_name"],
        phone=updated_user["phone"],
        email=updated_user["email"],
        role=updated_user["role"],
        disabled=updated_user["disabled"],
        created_at=updated_user["created_at"],
        updated_at=updated_user["updated_at"],
        message=None  # Default to None if no message
    )
    
    # Include the dynamic message if email update was blocked
    if email_update_blocked and remaining_days is not None:
        user_response.message = f"Email update blocked. Other fields have been updated. {remaining_days} days left."

    return user_response

