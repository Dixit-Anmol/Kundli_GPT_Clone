from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Optional, Dict, Any
from core.auth import get_current_user, require_current_user, verify_firebase_token
from pydantic import BaseModel

router = APIRouter()

class TokenVerifyRequest(BaseModel):
    token: str

@router.post("/auth/verify")
def verify_token_endpoint(req: TokenVerifyRequest):
    """Endpoint for verifying Firebase ID token and returning user profile claims."""
    claims = verify_firebase_token(req.token)
    return {
        "success": True,
        "user": claims
    }

@router.get("/auth/me")
def get_me(user: Dict[str, Any] = Depends(require_current_user)):
    """Protected endpoint returning the authenticated user profile."""
    return {
        "success": True,
        "user": user
    }
