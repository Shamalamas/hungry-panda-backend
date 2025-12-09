from fastapi import APIRouter, HTTPException, status
from app.models.schemas import UserResponse
from typing import List

router = APIRouter()

# Temporary in-memory storage
users_db = []

@router.get("/", response_model=List[UserResponse])
async def get_all_users():
    """Get all users"""
    return users_db

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Get user by ID"""
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, username: str = None, full_name: str = None):
    """Update user profile"""
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if username:
        user["username"] = username
    if full_name:
        user["full_name"] = full_name
    
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    """Delete user account"""
    global users_db
    users_db = [u for u in users_db if u["id"] != user_id]
    return None