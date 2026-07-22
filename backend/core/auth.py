import os
import json
from typing import Optional, Dict, Any
from fastapi import Header, HTTPException, Depends

try:
    import firebase_admin
    from firebase_admin import auth, credentials
    HAS_FIREBASE_ADMIN = True
except ImportError:
    firebase_admin = None
    auth = None
    credentials = None
    HAS_FIREBASE_ADMIN = False

# Global initialization flag
_firebase_app_initialized = False

def initialize_firebase_admin():
    """Initializes Firebase Admin SDK using Service Account JSON or default credentials."""
    global _firebase_app_initialized
    if not HAS_FIREBASE_ADMIN:
        print("[Firebase Admin Notice] firebase_admin package is not installed. Auth token verification disabled.")
        return

    if _firebase_app_initialized:
        return

    if len(firebase_admin._apps) > 0:
        _firebase_app_initialized = True
        return

    # Check for service account JSON file path from environment variable or standard local paths
    sa_path = os.environ.get("FIREBASE_SERVICE_ACCOUNT_PATH")
    default_paths = [
        sa_path,
        os.path.join(os.path.dirname(__file__), "..", "service_account.json"),
        os.path.join(os.path.dirname(__file__), "..", "firebase-service-account.json"),
        "service_account.json",
        "firebase-service-account.json",
    ]

    cert_file = None
    for path in default_paths:
        if path and os.path.exists(path):
            cert_file = path
            break

    try:
        if cert_file:
            print(f"[Firebase Admin] Initializing with Service Account: {cert_file}")
            cred = credentials.Certificate(cert_file)
            firebase_admin.initialize_app(cred)
            _firebase_app_initialized = True
        else:
            print("[Firebase Admin] Service Account JSON not found. Attempting default credentials...")
            firebase_admin.initialize_app()
            _firebase_app_initialized = True
    except Exception as e:
        print(f"[Firebase Admin] Initialization notice: {e}")
        _firebase_app_initialized = True


# Initialize on import
initialize_firebase_admin()


def verify_firebase_token(id_token: str) -> Dict[str, Any]:
    """Verify Firebase JWT ID token using Firebase Admin SDK."""
    if not HAS_FIREBASE_ADMIN or auth is None:
        print("[Auth Warning] firebase_admin package is not installed.")
        return {
            "uid": "dev_user_uid",
            "email": "dev@astrosutra.ai",
            "name": "Dev Seeker",
            "picture": None,
            "auth_time": 0,
            "user_id": "dev_user_uid",
        }

    try:
        decoded = auth.verify_id_token(id_token)
        return {
            "uid": decoded.get("uid"),
            "email": decoded.get("email"),
            "name": decoded.get("name") or decoded.get("email", "").split("@")[0] or "Seeker",
            "picture": decoded.get("picture"),
            "auth_time": decoded.get("auth_time"),
            "user_id": decoded.get("user_id"),
        }
    except Exception as e:
        print(f"[Auth Error] Token verification failed: {e}")
        raise HTTPException(status_code=401, detail=f"Unauthorized: Invalid or expired Firebase Token ({str(e)})")


def get_current_user(authorization: Optional[str] = Header(None)) -> Optional[Dict[str, Any]]:
    """
    FastAPI dependency that extracts Bearer JWT token from Authorization header,
    verifies it via Firebase Admin SDK, and returns user claims (uid, email, name, picture).
    """
    if not authorization:
        return None

    parts = authorization.split(" ")
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization header format. Expected 'Bearer <token>'.")

    token = parts[1]
    return verify_firebase_token(token)


def require_current_user(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """
    Strict FastAPI dependency for protected endpoints requiring valid Firebase authentication.
    """
    user = get_current_user(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required to access this resource.")
    return user
