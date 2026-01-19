import os
import uuid
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "dev_secret")
JWT_ALG = "HS256"
APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:5173")

bearer = HTTPBearer(auto_error=False)

app = FastAPI()

cors_origin = os.getenv("CORS_ORIGIN", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in cors_origin.split(",") if o.strip()],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

USERS_BY_EMAIL = {}
MAGIC_TOKENS = {}

STARTUPS = [
    {"id": "s1", "name": "EcoFlow", "industry": "Clean Energy", "desc": "Portable power solutions for sustainable living."},
    {"id": "s2", "name": "MediLink", "industry": "HealthTech", "desc": "Connecting patients with healthcare providers instantly."},
    {"id": "s3", "name": "FinPilot", "industry": "FinTech", "desc": "AI tools for smarter personal finance."},
    {"id": "s4", "name": "AgroNova", "industry": "AgriTech", "desc": "Innovating agriculture through smart sensors."},
]

RESOURCES_PUBLIC = [
    {"title": "Harvard Business Review", "description": "Insights and best practices for management, strategy, and leadership.", "link": "https://hbr.org/", "type": "Business Strategy"},
    {"title": "Nielsen Norman Group", "description": "World-leading research and expert guidance on user experience (UX) design.", "link": "https://www.nngroup.com/", "type": "Design & UX"},
    {"title": "Khan Academy", "description": "Free courses and educational resources covering math, science, economics, and arts.", "link": "https://www.khanacademy.org/", "type": "General Education"},
    {"title": "Coursera", "description": "Online courses and specializations from top universities and companies worldwide.", "link": "https://www.coursera.org/", "type": "Professional Courses"},
    {"title": "The Economist", "description": "Global analysis of politics, current affairs, business, and finance.", "link": "https://www.economist.com/", "type": "Current Affairs"},
    {"title": "NASA Image and Video Library", "description": "High-resolution media resources covering space exploration and scientific discovery.", "link": "https://images.nasa.gov/", "type": "Science & Research"},
]

def create_access_token(user):
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user["id"],
        "email": user["email"],
        "username": user.get("username", ""),
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(days=7)).timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

def require_user(creds: HTTPAuthorizationCredentials | None = Depends(bearer)):
    if not creds or creds.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Missing token")
    try:
        payload = jwt.decode(creds.credentials, JWT_SECRET, algorithms=[JWT_ALG])
        return {
            "id": payload.get("sub"),
            "email": payload.get("email"),
            "username": payload.get("username", ""),
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/auth/request-magic-link")
async def request_magic_link(req: Request):
    body = await req.json()
    email = (body.get("email") or "").strip().lower()
    username = (body.get("username") or "").strip()
    if not email or not username:
        raise HTTPException(status_code=400, detail="Invalid input")

    user = USERS_BY_EMAIL.get(email)
    if not user:
        user = {"id": f"u_{uuid.uuid4()}", "email": email, "username": username}
        USERS_BY_EMAIL[email] = user
    else:
        user["username"] = username

    token = f"ml_{uuid.uuid4()}"
    MAGIC_TOKENS[token] = {
        "email": email,
        "expires_at": datetime.now(timezone.utc) + timedelta(minutes=15),
    }

    return {"magic_link": f"{APP_BASE_URL}/JoinNow?token={token}"}

@app.get("/auth/verify")
def verify_magic_link(token: str):
    rec = MAGIC_TOKENS.get(token)
    if not rec or datetime.now(timezone.utc) > rec["expires_at"]:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = USERS_BY_EMAIL.get(rec["email"])
    MAGIC_TOKENS.pop(token, None)

    access_token = create_access_token(user)
    return {"access_token": access_token, "user": user}

@app.get("/startups")
def startups(query: str | None = None):
    q = (query or "").lower().strip()
    if not q:
        return {"items": STARTUPS}
    return {
        "items": [
            s for s in STARTUPS
            if q in s["name"].lower()
            or q in s["industry"].lower()
            or q in s["desc"].lower()
        ]
    }

@app.get("/resources/public")
def resources_public():
    return {"items": RESOURCES_PUBLIC}

@app.get("/resources")
def resources_private(user: dict = Depends(require_user)):
    return {"items": RESOURCES_PUBLIC}
