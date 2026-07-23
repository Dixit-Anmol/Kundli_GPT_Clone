"""
Module 6 — AI Reports Model.

Tables: ai_reports
Schema: ai
"""

import uuid
from datetime import datetime

from sqlalchemy import (
    CheckConstraint, ForeignKey, Index, Integer, Numeric, String, Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base, new_uuid


# ---------------------------------------------------------------------------
# 28. AI REPORTS
# ---------------------------------------------------------------------------
class AIReport(Base):
    __tablename__ = "ai_reports"
    __table_args__ = (
        CheckConstraint(
            "status IN ('generating','completed','failed','expired')",
            name="ck_report_status",
        ),
        Index("idx_reports_user", "user_id"),
        Index("idx_reports_type", "report_type"),
        Index("idx_reports_created", "created_at"),
        {"schema": "ai"},
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("platform.users.id", ondelete="CASCADE"), nullable=False
    )
    product_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("catalog.products.id")
    )
    astro_profile_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("astrology.astro_profiles.id")
    )
    report_type: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str | None] = mapped_column(String(255))
    content_markdown: Mapped[str | None] = mapped_column(Text)
    content_json: Mapped[dict | None] = mapped_column(JSONB)
    pdf_url: Mapped[str | None] = mapped_column(Text)
    version: Mapped[int] = mapped_column(Integer, default=1)
    ai_model: Mapped[str | None] = mapped_column(String(50))
    generation_time_ms: Mapped[int | None] = mapped_column(Integer)
    total_tokens: Mapped[int | None] = mapped_column(Integer)
    cost: Mapped[float | None] = mapped_column(Numeric(10, 6))
    status: Mapped[str] = mapped_column(String(20), default="completed")
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    expires_at: Mapped[datetime | None] = mapped_column()
