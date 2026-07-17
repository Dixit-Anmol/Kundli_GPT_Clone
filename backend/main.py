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
from api.profile import router as profile_router

app = FastAPI(
    title="Kundli AI API",
    description="Ancient Wisdom meets Modern Intelligence — Horoscope Computation and RAG-Gita Guided Chat Engine.",
    version="1.0.0"
)

# Enable CORS for React + Vite development server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://kundli-gpt-clone.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(chart_router, prefix="/api", tags=["Astrology & Timezone"])
app.include_router(chat_router, prefix="/api", tags=["Vedic Chat & RAG"])
app.include_router(profile_router, prefix="/api", tags=["Profile"])

@app.get("/")
def root():
    return {
        "status": "healthy",
        "service": "KundliGPT Astrological Compute Engine",
        "version": "1.0.0"
    }
