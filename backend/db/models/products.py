"""
Module 3 — Multi-Product Support Models.

Tables: products, user_products, product_features
Schema: catalog
"""

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean, CheckConstraint, ForeignKey, Index, Integer, SmallInteger,
    String, Text, UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base, TimestampMixin, new_uuid


# ---------------------------------------------------------------------------
# 11. PRODUCTS
# ---------------------------------------------------------------------------
class Product(Base, TimestampMixin):
    __tablename__ = "products"
    __table_args__ = (
        CheckConstraint(
            "status IN ('active','beta','deprecated','retired')",
            name="ck_products_status",
        ),
        {"schema": "catalog"},
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    slug: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    icon_url: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="active")
    launched_at: Mapped[datetime | None] = mapped_column()

    features = relationship("ProductFeature", back_populates="product", cascade="all, delete-orphan")


# ---------------------------------------------------------------------------
# 12. USER → PRODUCT access
# ---------------------------------------------------------------------------
class UserProduct(Base):
    __tablename__ = "user_products"
    __table_args__ = {"schema": "catalog"}

    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("platform.users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("catalog.products.id", ondelete="CASCADE"),
        primary_key=True,
    )
    access_level: Mapped[str] = mapped_column(String(20), default="standard")
    activated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    deactivated_at: Mapped[datetime | None] = mapped_column()


# ---------------------------------------------------------------------------
# 13. PRODUCT FEATURES
# ---------------------------------------------------------------------------
class ProductFeature(Base):
    __tablename__ = "product_features"
    __table_args__ = (
        UniqueConstraint("product_id", "slug", name="uq_product_feature_slug"),
        CheckConstraint(
            "tier_required IN ('free','standard','pro','enterprise')",
            name="ck_feature_tier",
        ),
        {"schema": "catalog"},
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    product_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("catalog.products.id", ondelete="CASCADE"), nullable=False
    )
    slug: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    tier_required: Mapped[str] = mapped_column(String(20), default="free")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    product = relationship("Product", back_populates="features")
