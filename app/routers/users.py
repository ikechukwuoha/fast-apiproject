import json
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from app.config.settings import settings
from app.schemas.users import UserCreate, UserResponse
from app.services.user_services import create_user, authenticate_user
from app.utils.security import create_access_token
from datetime import timedelta
from pydantic import BaseModel

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate):
    existing_user = authenticate_user(user_data.email, user_data.password)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = create_user(user_data)
    return user



class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login_user(request: LoginRequest):
    user = authenticate_user(request.email, request.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["email"]}, expires_delta=access_token_expires)
    
    # Set HTTP-only cookie with access token
    response = Response(
        content=json.dumps({"access_token": access_token, "token_type": "bearer"}),
        media_type="application/json"
    )
    response.set_cookie(
        "access_token",
        value=access_token,
        httponly=True,
        samesite="Strict",
        expires=access_token_expires  # Set expiration time
    )
    print("Cookie set:", response.headers.get("set-cookie"))  
    return response
