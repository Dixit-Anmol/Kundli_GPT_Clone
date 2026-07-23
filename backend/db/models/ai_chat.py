"""
Module 5 — AI Chat Models.

Tables: chat_sessions, chat_messages, chat_attachments, chat_feedback
Schema: ai
"""

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean, CheckConstraint, ForeignKey, Index, Integer,
    Numeric, SmallInteger, String, Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base, TimestampMixin, SoftDeleteMixin, new_uuid


# ---------------------------------------------------------------------------
# 24. CHAT SESSIONS
# ---------------------------------------------------------------------------
class ChatSession(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "chat_sessions"
    __table_args__ = (
        CheckConstraint(
            "status IN ('active','archived','deleted')",
            name="ck_chat_session_status",
        ),
        Index("idx_chat_sessions_user", "user_id"),
        Index("idx_chat_sessions_product", "product_id"),
        Index("idx_chat_sessions_created", "created_at"),
        {"schema": "ai"},
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("platform.users.id", ondelete="CASCADE"), nullable=False
    )
    product_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("catalog.products.id")
    )
    title: Mapped[str | None] = mapped_column(String(255))
    tab_context: Mapped[str | None] = mapped_column(String(50))
    astro_profile_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("astrology.astro_profiles.id")
    )
    model_used: Mapped[str | None] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(20), default="active")
    message_count: Mapped[int] = mapped_column(Integer, default=0)
    total_tokens: Mapped[int] = mapped_column(Integer, default=0)
    total_cost: Mapped[float] = mapped_column(Numeric(10, 6), default=0)
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)

    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")


# ---------------------------------------------------------------------------
# 25. CHAT MESSAGES
# ---------------------------------------------------------------------------
class ChatMessage(Base):
    __tablename__ = "chat_messages"
    __table_args__ = (
        CheckConstraint(
            "role IN ('user','assistant','system')",
            name="ck_message_role",
        ),
        Index("idx_messages_session", "session_id"),
        Index("idx_messages_role", "role"),
        Index("idx_messages_created", "created_at"),
        {"schema": "ai"},
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    session_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("ai.chat_sessions.id", ondelete="CASCADE"), nullable=False
    )
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    prompt_tokens: Mapped[int | None] = mapped_column(Integer)
    completion_tokens: Mapped[int | None] = mapped_column(Integer)
    total_tokens: Mapped[int | None] = mapped_column(Integer)
    model_used: Mapped[str | None] = mapped_column(String(50))
    temperature: Mapped[float | None] = mapped_column()
    latency_ms: Mapped[int | None] = mapped_column(Integer)
    cost: Mapped[float | None] = mapped_column(Numeric(10, 6))
    is_regenerated: Mapped[bool] = mapped_column(Boolean, default=False)
    parent_message_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("ai.chat_messages.id")
    )
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    edited_at: Mapped[datetime | None] = mapped_column()

    session = relationship("ChatSession", back_populates="messages")
    attachments = relationship("ChatAttachment", back_populates="message", cascade="all, delete-orphan")
    feedback = relationship("ChatFeedback", back_populates="message", cascade="all, delete-orphan")


# ---------------------------------------------------------------------------
# 26. CHAT ATTACHMENTS
# ---------------------------------------------------------------------------
class ChatAttachment(Base):
    __tablename__ = "chat_attachments"
    __table_args__ = {"schema": "ai"}

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    message_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("ai.chat_messages.id", ondelete="CASCADE"), nullable=False
    )
    file_asset_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("storage.file_assets.id")
    )
    file_type: Mapped[str | None] = mapped_column(String(20))
    file_url: Mapped[str | None] = mapped_column(Text)
    file_name: Mapped[str | None] = mapped_column(String(255))
    file_size_bytes: Mapped[int | None] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    message = relationship("ChatMessage", back_populates="attachments")


# ---------------------------------------------------------------------------
# 27. CHAT FEEDBACK
# ---------------------------------------------------------------------------
class ChatFeedback(Base):
    __tablename__ = "chat_feedback"
    __table_args__ = (
        Index("idx_feedback_message", "message_id"),
        {"schema": "ai"},
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    message_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("ai.chat_messages.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("platform.users.id", ondelete="CASCADE"), nullable=False
    )
    rating: Mapped[int | None] = mapped_column(SmallInteger)
    is_helpful: Mapped[bool | None] = mapped_column(Boolean)
    feedback_text: Mapped[str | None] = mapped_column(Text)
    feedback_type: Mapped[str] = mapped_column(String(30), default="general")
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    message = relationship("ChatMessage", back_populates="feedback")
