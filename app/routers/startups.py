from fastapi import APIRouter, HTTPException, status
from app.models.schemas import StartupCreate, StartupResponse, StartupUpdate
from typing import List
from datetime import datetime

router = APIRouter()

# Temporary in-memory storage
startups_db = []

@router.post("/", response_model=StartupResponse, status_code=status.HTTP_201_CREATED)
async def create_startup(startup: StartupCreate):
    """Create a new startup profile"""
    new_startup = {
        "id": len(startups_db) + 1,
        "name": startup.name,
        "description": startup.description,
        "industry": startup.industry,
        "stage": startup.stage,
        "website": startup.website,
        "logo_url": startup.logo_url,
        "owner_id": 1,  # Hardcoded for now, use authenticated user later
        "created_at": datetime.now().isoformat(),
        "updated_at": None
    }
    startups_db.append(new_startup)
    return new_startup

@router.get("/", response_model=List[StartupResponse])
async def get_all_startups(industry: str = None, stage: str = None):
    """Get all startups with optional filters"""
    filtered_startups = startups_db
    
    if industry:
        filtered_startups = [s for s in filtered_startups if s.get("industry") == industry]
    
    if stage:
        filtered_startups = [s for s in filtered_startups if s.get("stage") == stage]
    
    return filtered_startups

@router.get("/{startup_id}", response_model=StartupResponse)
async def get_startup(startup_id: int):
    """Get startup by ID"""
    startup = next((s for s in startups_db if s["id"] == startup_id), None)
    if not startup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Startup not found"
        )
    return startup

@router.put("/{startup_id}", response_model=StartupResponse)
async def update_startup(startup_id: int, startup_update: StartupUpdate):
    """Update startup profile"""
    startup = next((s for s in startups_db if s["id"] == startup_id), None)
    if not startup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Startup not found"
        )
    
    # Update only provided fields
    update_data = startup_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        startup[key] = value
    
    startup["updated_at"] = datetime.now().isoformat()
    return startup

@router.delete("/{startup_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_startup(startup_id: int):
    """Delete startup profile"""
    global startups_db
    startups_db = [s for s in startups_db if s["id"] != startup_id]
    return None