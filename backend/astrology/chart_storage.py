"""
Chart Storage / Caching Layer.

Stores generated FullChartBundle objects in memory and on disk.
Charts are only regenerated when birth details change or transit
data becomes stale.
"""

import os
import json
import threading
import datetime
from typing import Optional
from dataclasses import asdict

from backend.astrology.types import BirthDetails, FullChartBundle


# ---------------------------------------------------------------------------
# Storage directory
# ---------------------------------------------------------------------------
_STORAGE_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "data", "chart_bundles"
))
os.makedirs(_STORAGE_DIR, exist_ok=True)


class ChartCache:
    """
    Thread-safe in-memory + on-disk cache for FullChartBundle objects.

    Usage:
        chart_cache.store("user123", bundle)
        bundle = chart_cache.load("user123")
        if chart_cache.should_regenerate("user123", new_birth_details):
            ...
    """

    def __init__(self):
        self._memory: dict = {}
        self._lock = threading.Lock()

    # ---------------------------------------------------------------
    # Store
    # ---------------------------------------------------------------
    def store(self, user_id: str, bundle: FullChartBundle) -> None:
        """Cache the bundle in memory and persist to disk."""
        bundle_dict = bundle.to_dict()

        with self._lock:
            self._memory[user_id] = bundle_dict

        # Persist to disk
        filepath = os.path.join(_STORAGE_DIR, f"{user_id}.json")
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(bundle_dict, f, ensure_ascii=False, default=str)
        except Exception as e:
            print(f"[ChartCache] Failed to persist bundle for {user_id}: {e}")

    # ---------------------------------------------------------------
    # Load
    # ---------------------------------------------------------------
    def load(self, user_id: str) -> Optional[dict]:
        """
        Load a cached bundle (returns dict, not dataclass).
        Checks memory first, then disk.
        """
        with self._lock:
            if user_id in self._memory:
                return self._memory[user_id]

        # Try disk
        filepath = os.path.join(_STORAGE_DIR, f"{user_id}.json")
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                with self._lock:
                    self._memory[user_id] = data
                return data
            except Exception as e:
                print(f"[ChartCache] Failed to load bundle for {user_id}: {e}")

        return None

    # ---------------------------------------------------------------
    # Should Regenerate?
    # ---------------------------------------------------------------
    def should_regenerate(
        self,
        user_id: str,
        new_birth: BirthDetails,
        max_transit_age_hours: int = 24,
    ) -> bool:
        """
        Determine whether charts need to be regenerated.

        Returns True if:
        1. No cached bundle exists.
        2. Birth details have changed.
        3. Transit (gochar) data is older than max_transit_age_hours.
        """
        cached = self.load(user_id)
        if cached is None:
            return True

        # Check birth details
        cached_birth = cached.get("birth_details", {})
        if (
            cached_birth.get("date_of_birth") != new_birth.date_of_birth
            or cached_birth.get("time_of_birth") != new_birth.time_of_birth
            or cached_birth.get("latitude") != new_birth.latitude
            or cached_birth.get("longitude") != new_birth.longitude
            or cached_birth.get("timezone_offset") != new_birth.timezone_offset
        ):
            return True

        # Check transit freshness
        generated_at = cached.get("generated_at", "")
        if generated_at:
            try:
                gen_dt = datetime.datetime.fromisoformat(generated_at)
                age = datetime.datetime.utcnow() - gen_dt
                if age.total_seconds() > max_transit_age_hours * 3600:
                    return True
            except Exception:
                return True

        return False

    # ---------------------------------------------------------------
    # Invalidate
    # ---------------------------------------------------------------
    def invalidate(self, user_id: str) -> None:
        """Remove cached data for a user."""
        with self._lock:
            self._memory.pop(user_id, None)

        filepath = os.path.join(_STORAGE_DIR, f"{user_id}.json")
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception:
                pass

    # ---------------------------------------------------------------
    # Update Transit Data Only
    # ---------------------------------------------------------------
    def refresh_transits(self, user_id: str, gochar_dict: dict) -> None:
        """
        Update only the gochar (transit) portion without regenerating
        the entire natal chart bundle.
        """
        cached = self.load(user_id)
        if cached is None:
            return

        cached["gochar"] = gochar_dict
        cached["generated_at"] = datetime.datetime.utcnow().isoformat()

        with self._lock:
            self._memory[user_id] = cached

        # Persist
        filepath = os.path.join(_STORAGE_DIR, f"{user_id}.json")
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(cached, f, ensure_ascii=False, default=str)
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Global singleton
# ---------------------------------------------------------------------------
chart_cache = ChartCache()
