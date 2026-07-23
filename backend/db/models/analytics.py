"""
Modules 10 & 12 — Analytics & AI Analytics Models.

Tables: user_analytics_events, ai_analytics, system_metrics, user_daily_usage
Schema: analytics
"""

import uuid
from datetime import date, datetime

from sqlalchemy import (
    Boolean, Date, Float, ForeignKey, Index, Integer, Numeric,
    SmallInteger, String, Text,
)
from sqlalchemy.dialects.postgresql import ARRAY, INET, JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base, new_uuid


# ---------------------------------------------------------------------------
# 38. USER ANALYTICS EVENTS — Append-only event stream
# ---------------------------------------------------------------------------
class UserAnalyticsEvent(Base):
    __tablename__ = "user_analytics_events"
    __table_args__ = (
        Index("idx_analytics_user", "user_id"),
        Index("idx_analytics_event", "event_type"),
        Index("idx_analytics_created", "created_at"),
        Index("idx_analytics_product", "product_id"),
        {"schema": "analytics"},
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("platform.users.id", ondelete="SET NULL")
    )
    session_id: Mapped[uuid.UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    product_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("catalog.products.id")
    )
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    event_category: Mapped[str | None] = mapped_column(String(30))
    event_data: Mapped[dict] = mapped_column(JSONB, default=dict)
    page_url: Mapped[str | None] = mapped_column(Text)
    referrer: Mapped[str | None] = mapped_column(Text)
    ip_address: Mapped[str | None] = mapped_column(INET)
    country: Mapped[str | None] = mapped_column(String(3))
    city: Mapped[str | None] = mapped_column(String(100))
    device_type: Mapped[str | None] = mapped_column(String(20))
    browser: Mapped[str | None] = mapped_column(String(50))
    os: Mapped[str | None] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


# ---------------------------------------------------------------------------
# 39. SYSTEM METRICS — Periodic system health snapshots
# ---------------------------------------------------------------------------
class SystemMetric(Base):
    __tablename__ = "system_metrics"
    __table_args__ = (
        Index("idx_system_metrics_name", "metric_name"),
        Index("idx_system_metrics_time", "recorded_at"),
        {"schema": "analytics"},
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    metric_name: Mapped[str] = mapped_column(String(100), nullable=False)
    metric_value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str | None] = mapped_column(String(20))
    tags: Mapped[dict] = mapped_column(JSONB, default=dict)
    recorded_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


# ---------------------------------------------------------------------------
# 41. AI ANALYTICS — Per-interaction tracking (Module 12)
# ---------------------------------------------------------------------------
class AIAnalytics(Base):
    __tablename__ = "ai_analytics"
    __table_args__ = (
        Index("idx_ai_analytics_user", "user_id"),
        Index("idx_ai_analytics_model", "model_used"),
        Index("idx_ai_analytics_created", "created_at"),
        Index("idx_ai_analytics_success", "is_success"),
        {"schema": "analytics"},
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("platform.users.id", ondelete="SET NULL")
    )
    session_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("ai.chat_sessions.id", ondelete="SET NULL")
    )
    message_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("ai.chat_messages.id", ondelete="SET NULL")
    )
    product_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("catalog.products.id")
    )
    prompt_text: Mapped[str | None] = mapped_column(Text)
    prompt_category: Mapped[str | None] = mapped_column(String(50))
    prompt_tags: Mapped[list | None] = mapped_column(ARRAY(String(255)))
    response_text: Mapped[str | None] = mapped_column(Text)
    response_rating: Mapped[int | None] = mapped_column(SmallInteger)
    feedback_text: Mapped[str | None] = mapped_column(Text)
    model_used: Mapped[str | None] = mapped_column(String(50))
    prompt_tokens: Mapped[int | None] = mapped_column(Integer)
    completion_tokens: Mapped[int | None] = mapped_column(Integer)
    total_tokens: Mapped[int | None] = mapped_column(Integer)
    prompt_length: Mapped[int | None] = mapped_column(Integer)
    response_length: Mapped[int | None] = mapped_column(Integer)
    time_to_first_token_ms: Mapped[int | None] = mapped_column(Integer)
    total_generation_time_ms: Mapped[int | None] = mapped_column(Integer)
    latency_ms: Mapped[int | None] = mapped_column(Integer)
    cost: Mapped[float | None] = mapped_column(Numeric(10, 6))
    is_success: Mapped[bool] = mapped_column(Boolean, default=True)
    error_type: Mapped[str | None] = mapped_column(String(50))
    error_message: Mapped[str | None] = mapped_column(Text)
    regeneration_count: Mapped[int] = mapped_column(SmallInteger, default=0)
    conversation_length: Mapped[int | None] = mapped_column(Integer)
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


# ---------------------------------------------------------------------------
# 47. USER DAILY USAGE — Materialized daily aggregates
# ---------------------------------------------------------------------------
class UserDailyUsage(Base):
    __tablename__ = "user_daily_usage"
    __table_args__ = (
        Index("idx_daily_usage_user", "user_id"),
        Index("idx_daily_usage_date", "usage_date"),
        {"schema": "analytics"},
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("platform.users.id", ondelete="CASCADE"), nullable=False
    )
    product_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("catalog.products.id")
    )
    usage_date: Mapped[date] = mapped_column(Date, nullable=False)
    chat_count: Mapped[int] = mapped_column(Integer, default=0)
    reports_generated: Mapped[int] = mapped_column(Integer, default=0)
    tokens_consumed: Mapped[int] = mapped_column(Integer, default=0)
    api_calls: Mapped[int] = mapped_column(Integer, default=0)
    active_minutes: Mapped[int] = mapped_column(Integer, default=0)
    cost_incurred: Mapped[float] = mapped_column(Numeric(10, 6), default=0)
