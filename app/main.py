from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, startups, resources, users
from app.core.config import settings

app = FastAPI(
    title="Hungry Panda API",
    description="Empowering startups to learn, build, fund, and grow",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(startups.router, prefix="/api/startups", tags=["Startups"])
app.include_router(resources.router, prefix="/api/resources", tags=["Resources"])

@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Entrepreneurship Hub API running successfully 🚀",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "API is running"}