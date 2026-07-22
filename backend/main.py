import os
import sys
from dotenv import load_dotenv

# Ensure both backend directory and project root are in python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(backend_dir, ".."))
sys.path.insert(0, backend_dir)
sys.path.insert(0, project_root)

# Load environment variables from .env file before other imports
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.chart import router as chart_router
from api.chat import router as chat_router
from api.tab_chat import router as tab_chat_router
from api.profile import router as profile_router
from api.matching import router as matching_router
from api.dasha import router as dasha_router

app = FastAPI(
    title="AstroSutra AI API",
    description="Ancient Wisdom meets Modern Intelligence — Horoscope Computation and RAG-Gita Guided Chat Engine.",
    version="1.0.0"
)

frontend_url_env = os.environ.get("FRONTEND_URL")

origins = [
    "https://astrosutraai.onrender.com",
    "https://astrosutraai.onrender.com/",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

if frontend_url_env:
    raw_env = frontend_url_env.strip()
    clean_env = raw_env.rstrip("/")
    if clean_env not in origins:
        origins.append(clean_env)
    if (clean_env + "/") not in origins:
        origins.append(clean_env + "/")

# Enable CORS for React + Vite frontend server & Astrosutra domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*astrosutra.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(chart_router, prefix="/api", tags=["Astrology & Timezone"])
app.include_router(chat_router, prefix="/api", tags=["Vedic Chat & RAG"])
app.include_router(tab_chat_router, prefix="/api", tags=["Tab-Scoped Chat"])
app.include_router(profile_router, prefix="/api", tags=["Profile"])
app.include_router(matching_router, prefix="/api", tags=["Kundli Matching"])
app.include_router(dasha_router, prefix="/api", tags=["Dasha Timeline"])

@app.get("/")
def root():
    return {
        "status": "healthy",
        "service": "KundliGPT Astrological Compute Engine",
        "version": "1.0.0"
    }
