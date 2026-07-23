"""
Module 1 — Identity Models.

Tables: users, auth_providers, user_profiles, user_preferences, user_devices, user_sessions
Schema: platform
"""

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean, Column, Date, ForeignKey, Index, Integer, String, Text,
    CheckConstraint, UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import INET, JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base, TimestampMixin, SoftDeleteMixin, new_uuid


# ---------------------------------------------------------------------------
# 1. USERS — Central identity anchor
# ---------------------------------------------------------------------------
class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint(
            "status IN ('active','suspended','deactivated','banned')",
            name="ck_users_status",
        ),
        Index("idx_users_firebase_uid", "firebase_uid"),
        Index("idx_users_email", "email"),
        Index("idx_users_status", "status", postgresql_where="deleted_at IS NULL"),
        Index("idx_users_created_at", "created_at"),
        {"schema": "platform"},
    )

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=new_uuid
    )
    firebase_uid: Mapped[str | None] = mapped_column(String(128), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    display_name: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(20))
    profile_picture: Mapped[str | None] = mapped_column(Text)
    language: Mapped[str] = mapped_column(String(10), default="en")
    timezone: Mapped[str] = mapped_column(String(50), default="Asia/Kolkata")
    country: Mapped[str | None] = mapped_column(String(3))
    status: Mapped[str] = mapped_column(String(20), default="active")
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    last_login_at: Mapped[datetime | None] = mapped_column()
    last_login_ip: Mapped[str | None] = mapped_column(INET)

    # Relationships
    auth_providers = relationship("AuthProvider", back_populates="user", cascade="all, delete-orphan")
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    preferences = relationship("UserPreference", back_populates="user", uselist=False, cascade="all, delete-orphan")
    devices = relationship("UserDevice", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")


# ---------------------------------------------------------------------------
# 2. AUTH PROVIDERS — Multiple login methods per user
# ---------------------------------------------------------------------------
class AuthProvider(Base):
    __tablename__ = "auth_providers"
    __table_args__ = (
        CheckConstraint(
            "provider IN ('google','email','apple','microsoft','github','phone')",
            name="ck_auth_provider_type",
        ),
        UniqueConstraint("provider", "provider_uid", name="uq_auth_provider_uid"),
        Index("idx_auth_providers_user", "user_id"),
        {"schema": "platform"},
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("platform.users.id", ondelete="CASCADE"), nullable=False
    )
    provider: Mapped[str] = mapped_column(String(30), nullable=False)
    provider_uid: Mapped[str] = mapped_column(String(255), nullable=False)
    provider_email: Mapped[str | None] = mapped_column(String(255))
    provider_data: Mapped[dict] = mapped_column(JSONB, default=dict)
    linked_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user = relationship("User", back_populates="auth_providers")


# ---------------------------------------------------------------------------
# 3. USER PROFILES — Extended profile data
# ---------------------------------------------------------------------------
class UserProfile(Base, TimestampMixin):
    __tablename__ = "user_profiles"
    __table_args__ = {"schema": "platform"}

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("platform.users.id", ondelete="CASCADE"),
        unique=True, nullable=False,
    )
    bio: Mapped[str | None] = mapped_column(Text)
    date_of_birth: Mapped[datetime | None] = mapped_column(Date)
    gender: Mapped[str | None] = mapped_column(String(10))
    occupation: Mapped[str | None] = mapped_column(String(100))
    city: Mapped[str | None] = mapped_column(String(100))
    state: Mapped[str | None] = mapped_column(String(100))
    country: Mapped[str | None] = mapped_column(String(3))
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)

    user = relationship("User", back_populates="profile")


# ---------------------------------------------------------------------------
# 4. USER PREFERENCES
# ---------------------------------------------------------------------------
class UserPreference(Base, TimestampMixin):
    __tablename__ = "user_preferences"
    __table_args__ = {"schema": "platform"}

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("platform.users.id", ondelete="CASCADE"),
        unique=True, nullable=False,
    )
    theme: Mapped[str] = mapped_column(String(20), default="system")
    notifications_email: Mapped[bool] = mapped_column(Boolean, default=True)
    notifications_push: Mapped[bool] = mapped_column(Boolean, default=True)
    notifications_sms: Mapped[bool] = mapped_column(Boolean, default=False)
    ai_language: Mapped[str] = mapped_column(String(10), default="en")
    ai_response_style: Mapped[str] = mapped_column(String(20), default="balanced")
    custom_settings: Mapped[dict] = mapped_column(JSONB, default=dict)

    user = relationship("User", back_populates="preferences")
