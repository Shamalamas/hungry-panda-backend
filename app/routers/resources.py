from fastapi import APIRouter, HTTPException, status
from app.models.schemas import ResourceCreate, ResourceResponse
from typing import List
from datetime import datetime

router = APIRouter()

# Temporary in-memory storage
resources_db = []

@router.post("/", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
async def create_resource(resource: ResourceCreate):
    """Create a new resource"""
    new_resource = {
        "id": len(resources_db) + 1,
        "title": resource.title,
        "description": resource.description,
        "category": resource.category,
        "url": resource.url,
        "content": resource.content,
        "created_at": datetime.now().isoformat(),
        "views": 0
    }
    resources_db.append(new_resource)
    return new_resource

@router.get("/", response_model=List[ResourceResponse])
async def get_all_resources(category: str = None):
    """Get all resources with optional category filter"""
    if category:
        return [r for r in resources_db if r["category"] == category]
    return resources_db

@router.get("/categories", response_model=List[str])
async def get_categories():
    """Get all unique resource categories"""
    categories = list(set(r["category"] for r in resources_db))
    return categories

@router.get("/{resource_id}", response_model=ResourceResponse)
async def get_resource(resource_id: int):
    """Get resource by ID"""
    resource = next((r for r in resources_db if r["id"] == resource_id), None)
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    
    # Increment view count
    resource["views"] += 1
    return resource

@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resource(resource_id: int):
    """Delete resource"""
    global resources_db
    resources_db = [r for r in resources_db if r["id"] != resource_id]
    return None