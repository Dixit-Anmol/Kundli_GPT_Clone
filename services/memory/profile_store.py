"""
Persistent profile storage using JSON files on disk.

Each user profile is stored as {user_id}.json in the profiles directory.
Profiles survive server restarts and contain natal chart data + birth details.
"""

import os
import json
import tempfile
import threading
from datetime import datetime, timezone


# Resolve profiles directory relative to the backend/data folder
_BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PROFILES_DIR = os.path.join(
    os.path.dirname(_BACKEND_DIR),  # project root from services/
    "backend", "data", "profiles"
)


class ProfileStore:
    """Thread-safe JSON-file-based persistent storage for anonymous user profiles."""

    def __init__(self, profiles_dir: str = None):
        self.profiles_dir = profiles_dir or _PROFILES_DIR
        os.makedirs(self.profiles_dir, exist_ok=True)
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _path(self, user_id: str) -> str:
        """Return the absolute path to a user's profile JSON file."""
        # Sanitize to prevent directory traversal
        safe_id = "".join(c for c in user_id if c.isalnum() or c in "-_")
        return os.path.join(self.profiles_dir, f"{safe_id}.json")

    def _atomic_write(self, path: str, data: dict):
        """Write JSON atomically using tempfile + rename to avoid corruption."""
        dir_name = os.path.dirname(path)
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tmp", dir=dir_name, delete=False
        ) as tmp:
            json.dump(data, tmp, indent=2, default=str)
            tmp_path = tmp.name
        # Atomic rename (on Windows, need to remove target first)
        try:
            if os.path.exists(path):
                os.replace(tmp_path, path)
            else:
                os.rename(tmp_path, path)
        except OSError:
            # Fallback: direct overwrite if atomic rename fails
            import shutil
            shutil.move(tmp_path, path)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def has_profile(self, user_id: str) -> bool:
        """Check whether a profile exists for the given user ID."""
        return os.path.isfile(self._path(user_id))

    def save_profile(
        self,
        user_id: str,
        birth_details: dict,
        natal_chart: dict,
        chart_response: dict,
    ):
        """
        Persist a user profile to disk.

        Parameters
        ----------
        user_id : str
            The anonymous UUID from the client's localStorage.
        birth_details : dict
            Raw birth inputs: name, dob, tob, lat, lon, timezone_offset.
        natal_chart : dict
            The full natal chart context (planets, houses, yogas, doshas).
            This is the *static* portion — never recalculated unless details change.
        chart_response : dict
            The summary response sent back to the frontend (ascendant_sign, moon_sign, etc.).
        """
        now = datetime.now(timezone.utc).isoformat()

        profile = {
            "user_id": user_id,
            "birth_details": birth_details,
            "natal_chart": natal_chart,
            "chart_response": chart_response,
            "created_at": now,
            "updated_at": now,
        }

        # Preserve original creation timestamp if updating
        existing = self.load_profile(user_id)
        if existing and "created_at" in existing:
            profile["created_at"] = existing["created_at"]

        with self._lock:
            self._atomic_write(self._path(user_id), profile)

    def load_profile(self, user_id: str) -> dict | None:
        """
        Load a profile from disk. Returns None if not found or corrupted.
        """
        path = self._path(user_id)
        if not os.path.isfile(path):
            return None
        try:
            with self._lock:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"[ProfileStore] Corrupted profile for {user_id}: {e}")
            return None

    def delete_profile(self, user_id: str) -> bool:
        """Delete a profile from disk. Returns True if deleted, False if not found."""
        path = self._path(user_id)
        with self._lock:
            if os.path.isfile(path):
                os.remove(path)
                return True
        return False

    def update_profile(self, user_id: str, **updates):
        """
        Partially update fields in an existing profile.
        Useful for updating only natal_chart or chart_response without
        touching birth_details.
        """
        profile = self.load_profile(user_id)
        if not profile:
            return False

        for key, value in updates.items():
            if key in profile:
                profile[key] = value

        profile["updated_at"] = datetime.now(timezone.utc).isoformat()

        with self._lock:
            self._atomic_write(self._path(user_id), profile)
        return True


# Global singleton instance
profile_store = ProfileStore()
