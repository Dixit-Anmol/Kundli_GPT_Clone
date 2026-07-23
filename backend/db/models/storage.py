"""
Module 8 — File Storage Model.

Tables: file_assets
Schema: storage
"""

import uuid
from datetime import datetime

from sqlalchemy import (
    CheckConstraint, ForeignKey, Index, String, Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base, SoftDeleteMixin, new_uuid


# ---------------------------------------------------------------------------
# 35. FILE ASSETS
# ---------------------------------------------------------------------------
class FileAsset(Base, SoftDeleteMixin):
    __tablename__ = "file_assets"
    __table_args__ = (
        CheckConstraint(
            "file_type IN ('image','audio','video','pdf','document','avatar','report')",
            name="ck_file_type",
        ),
        Index("idx_files_user", "user_id"),
        Index("idx_files_type", "file_type"),
        {"schema": "storage"},
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("platform.users.id", ondelete="CASCADE"), nullable=False
    )
    product_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("catalog.products.id")
    )
    file_type: Mapped[str] = mapped_column(String(20), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[str | None] = mapped_column(String(100))
    file_size_bytes: Mapped[int | None] = mapped_column()
    storage_path: Mapped[str] = mapped_column(Text, nullable=False)
    public_url: Mapped[str | None] = mapped_column(Text)
    thumbnail_url: Mapped[str | None] = mapped_column(Text)
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
