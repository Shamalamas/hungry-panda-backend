from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    is_active: bool = True
    
    class Config:
        from_attributes = True

# Startup Schemas
class StartupBase(BaseModel):
    name: str
    description: str
    industry: Optional[str] = None
    stage: Optional[str] = None  # e.g., "Idea", "MVP", "Growth"
    website: Optional[str] = None
    logo_url: Optional[str] = None

class StartupCreate(StartupBase):
    pass

class StartupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    stage: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None

class StartupResponse(StartupBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Resource Schemas
class ResourceBase(BaseModel):
    title: str
    description: str
    category: str  # e.g., "Funding", "Learning", "Tools"
    url: Optional[str] = None
    content: Optional[str] = None

class ResourceCreate(ResourceBase):
    pass

class ResourceResponse(ResourceBase):
    id: int
    created_at: datetime
    views: int = 0
    
    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None