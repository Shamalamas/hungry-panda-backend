# hungry-panda-backend

🍜🐼 Hungry Panda Backend API

FastAPI backend for empowering startups to learn, build, fund, and grow

📋 Table of Contents

Overview
Tech Stack
Project Structure
Quick Start
API Documentation
API Endpoints
Configuration
Database Integration


🎯 Overview
RESTful API built with FastAPI providing:

🔐 User Authentication - Secure signup, login, and session management
🚀 Startup Profiles - Create and manage startup company profiles
📚 Resource Management - Curated learning resources for entrepreneurs
👤 User Management - Profile and preference handling

Currently using in-memory storage for rapid development, with planned migration to Supabase PostgreSQL.

🛠️ Tech Stack
TechnologyVersionPurposeFastAPI0.109.0Modern web framework for APIsPython3.10+Programming languagePydantic2.5.3Data validationUvicorn0.27.0ASGI serverSupabasePlannedPostgreSQL database

📁 Project Structure
backend/
├── app/
│   ├── main.py                  # FastAPI app entry point
│   ├── core/
│   │   └── config.py            # Settings & configuration
│   ├── models/
│   │   └── schemas.py           # Pydantic request/response models
│   └── routers/
│       ├── auth.py              # Authentication endpoints
│       ├── users.py             # User management
│       ├── startups.py          # Startup profiles
│       └── resources.py         # Learning resources
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
└── .gitignore                   # Git ignore rules

🚀 Quick Start
Prerequisites

Python 3.10+
pip
Git

Installation
bash# 1. Clone and navigate
git clone https://github.com/<your-username>/hungry-panda.git
cd hungry-panda/backend

# 2. Create directory structure
mkdir -p app/core app/models app/routers

# 3. Create __init__.py files
touch app/__init__.py app/core/__init__.py app/models/__init__.py app/routers/__init__.py

# 4. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt

# 6. Setup environment
cp .env.example .env
# Edit .env and update SECRET_KEY

# 7. Run server
uvicorn app.main:app --reload
Verify Installation
Open http://127.0.0.1:8000 - you should see:
json{
  "message": "Entrepreneurship Hub API running successfully 🚀",
  "version": "1.0.0",
  "status": "healthy"
}

📚 API Documentation
FastAPI auto-generates interactive documentation:

Swagger UI: http://127.0.0.1:8000/docs (Interactive testing)
ReDoc: http://127.0.0.1:8000/redoc (Clean documentation)


🔌 API Endpoints
Authentication (/api/auth)
MethodEndpointDescriptionPOST/api/auth/signupRegister new userPOST/api/auth/loginUser loginPOST/api/auth/logoutUser logoutGET/api/auth/meGet current user
Example Request:
jsonPOST /api/auth/signup
{
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "password": "securePass123"
}
Example Response:
json{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "created_at": "2024-01-01T00:00:00",
  "is_active": true
}
Users (/api/users)
MethodEndpointDescriptionGET/api/users/Get all usersGET/api/users/{id}Get user by IDPUT/api/users/{id}Update userDELETE/api/users/{id}Delete user
Startups (/api/startups)
MethodEndpointDescriptionPOST/api/startups/Create startupGET/api/startups/Get all startupsGET/api/startups/{id}Get startup by IDPUT/api/startups/{id}Update startupDELETE/api/startups/{id}Delete startup
Query Parameters:

industry - Filter by industry (e.g., ?industry=FinTech)
stage - Filter by stage (e.g., ?stage=MVP)

Example:
jsonPOST /api/startups/
{
  "name": "TechVenture",
  "description": "AI-powered analytics",
  "industry": "SaaS",
  "stage": "MVP",
  "website": "https://techventure.com"
}
Resources (/api/resources)
MethodEndpointDescriptionPOST/api/resources/Create resourceGET/api/resources/Get all resourcesGET/api/resources/categoriesGet categoriesGET/api/resources/{id}Get resource by IDDELETE/api/resources/{id}Delete resource
Query Parameters:

category - Filter by category (e.g., ?category=Funding)

Categories: Funding, Learning, Tools, Networking, Legal

⚙️ Configuration
Environment Variables (.env)
env# App Configuration
APP_NAME=Hungry Panda API
DEBUG=True

# CORS - Frontend URLs (comma-separated)
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# JWT Authentication
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database (Future)
DATABASE_URL=
SUPABASE_URL=
SUPABASE_KEY=
Generate Secure SECRET_KEY
pythonimport secrets
print(secrets.token_urlsafe(32))
CORS Configuration
Pre-configured for:

http://localhost:5173 (Vite dev server)
http://127.0.0.1:5173
http://localhost:3000

Add more origins in .env or app/core/config.py.

💾 Database Integration
Current: In-Memory Storage
✅ Fast development and testing
✅ No setup required
❌ Data lost on restart
❌ Not production-ready
Future: Supabase Migration
Setup Steps:

Create Supabase Project at supabase.com
Install Client:

bash   pip install supabase

Update .env:

env   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-key

Create Tables:

sql   -- Users
   CREATE TABLE users (
     id SERIAL PRIMARY KEY,
     email VARCHAR(255) UNIQUE NOT NULL,
     username VARCHAR(100) UNIQUE NOT NULL,
     full_name VARCHAR(255),
     password_hash VARCHAR(255) NOT NULL,
     created_at TIMESTAMP DEFAULT NOW(),
     is_active BOOLEAN DEFAULT TRUE
   );

   -- Startups
   CREATE TABLE startups (
     id SERIAL PRIMARY KEY,
     name VARCHAR(255) NOT NULL,
     description TEXT,
     industry VARCHAR(100),
     stage VARCHAR(50),
     website VARCHAR(255),
     logo_url VARCHAR(255),
     owner_id INTEGER REFERENCES users(id),
     created_at TIMESTAMP DEFAULT NOW(),
     updated_at TIMESTAMP
   );

   -- Resources
   CREATE TABLE resources (
     id SERIAL PRIMARY KEY,
     title VARCHAR(255) NOT NULL,
     description TEXT,
     category VARCHAR(100) NOT NULL,
     url VARCHAR(255),
     content TEXT,
     views INTEGER DEFAULT 0,
     created_at TIMESTAMP DEFAULT NOW()
   );

Update routers to use Supabase queries instead of in-memory lists


🔧 Development Tips
Common Commands
bash# Run server with auto-reload
uvicorn app.main:app --reload

# Freeze dependencies
pip freeze > requirements.txt

# Deactivate environment
deactivate
Adding New Endpoints

Define schema in app/models/schemas.py
Create router in app/routers/
Register in app/main.py

Troubleshooting
IssueSolutionModuleNotFoundErrorActivate venv and run pip install -r requirements.txtPort already in useUse different port: uvicorn app.main:app --port 8001 --reloadCORS errorsCheck ALLOWED_ORIGINS in .env

Happy Coding! 🍜🐼
Built with FastAPI • Python 3.10+ • AWS