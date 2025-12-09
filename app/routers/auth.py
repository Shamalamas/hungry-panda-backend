from fastapi import APIRouter, HTTPException, status
from app.models.schemas import UserCreate, UserLogin, UserResponse, Token

router = APIRouter()

# Temporary in-memory storage (replace with database later)
users_db = []

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate):
    """Register a new user"""
    # Check if user already exists
    if any(u["email"] == user.email for u in users_db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user (in real app, hash password here)
    new_user = {
        "id": len(users_db) + 1,
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
        "created_at": "2024-01-01T00:00:00",
        "is_active": True
    }
    users_db.append(new_user)
    
    return new_user

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """Login user and return access token"""
    # Find user (in real app, verify hashed password)
    user = next((u for u in users_db if u["email"] == credentials.email), None)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # In real app, generate JWT token here
    return {
        "access_token": f"fake_token_for_{user['email']}",
        "token_type": "bearer"
    }

@router.post("/logout")
async def logout():
    """Logout user (invalidate token)"""
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserResponse)
async def get_current_user():
    """Get current authenticated user"""
    # In real app, decode JWT token and get user from database
    if not users_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return users_db[0]  # Return first user for demo