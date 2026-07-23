"""
Module 9 — Notifications Models.

Tables: notifications, notification_preferences
Schema: comms
"""

import uuid
from datetime import datetime, time

from sqlalchemy import (
    Boolean, CheckConstraint, ForeignKey, Index, String, Text, Time,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base, new_uuid


# ---------------------------------------------------------------------------
# 36. NOTIFICATIONS
# ---------------------------------------------------------------------------
class Notification(Base):
    __tablename__ = "notifications"
    __table_args__ = (
        CheckConstraint(
            "channel IN ('email','push','sms','in_app')",
            name="ck_notification_channel",
        ),
        Index("idx_notifications_user", "user_id"),
        Index("idx_notifications_unread", "user_id", "is_read", postgresql_where="is_read = FALSE"),
        {"schema": "comms"},
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("platform.users.id", ondelete="CASCADE"), nullable=False
    )
    channel: Mapped[str] = mapped_column(String(20), nullable=False)
    title: Mapped[str | None] = mapped_column(String(255))
    body: Mapped[str | None] = mapped_column(Text)
    action_url: Mapped[str | None] = mapped_column(Text)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    read_at: Mapped[datetime | None] = mapped_column()
    sent_at: Mapped[datetime | None] = mapped_column()
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


# ---------------------------------------------------------------------------
# 37. NOTIFICATION PREFERENCES
# ---------------------------------------------------------------------------
class NotificationPreference(Base):
    __tablename__ = "notification_preferences"
    __table_args__ = (
        CheckConstraint(
            "digest_frequency IN ('instant','daily','weekly','none')",
            name="ck_digest_frequency",
        ),
        {"schema": "comms"},
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("platform.users.id", ondelete="CASCADE"),
        unique=True, nullable=False,
    )
    email_marketing: Mapped[bool] = mapped_column(Boolean, default=True)
    email_transactional: Mapped[bool] = mapped_column(Boolean, default=True)
    push_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    sms_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    digest_frequency: Mapped[str] = mapped_column(String(20), default="daily")
    quiet_hours_start: Mapped[time | None] = mapped_column(Time)
    quiet_hours_end: Mapped[time | None] = mapped_column(Time)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
