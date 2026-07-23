"""
Module 7 — Subscriptions & Billing Models.

Tables: subscription_plans, subscriptions, coupons, invoices, payments, transaction_history
Schema: billing
"""

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean, CheckConstraint, ForeignKey, Index, Integer, Numeric,
    SmallInteger, String, Text,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base, TimestampMixin, new_uuid


# ---------------------------------------------------------------------------
# 29. SUBSCRIPTION PLANS
# ---------------------------------------------------------------------------
class SubscriptionPlan(Base, TimestampMixin):
    __tablename__ = "subscription_plans"
    __table_args__ = (
        CheckConstraint(
            "tier IN ('free','standard','pro','enterprise')",
            name="ck_plan_tier",
        ),
        {"schema": "billing"},
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    slug: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    tier: Mapped[str] = mapped_column(String(20), nullable=False)
    price_monthly: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    price_yearly: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    currency: Mapped[str] = mapped_column(String(3), default="INR")
    features: Mapped[dict] = mapped_column(JSONB, default=dict)
    limits: Mapped[dict] = mapped_column(JSONB, default=dict)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(SmallInteger, default=0)

    subscriptions = relationship("Subscription", back_populates="plan")


# ---------------------------------------------------------------------------
# 31. COUPONS (declared before Subscription for FK reference)
# ---------------------------------------------------------------------------
class Coupon(Base):
    __tablename__ = "coupons"
    __table_args__ = (
        CheckConstraint(
            "discount_type IN ('percent','fixed')",
            name="ck_coupon_discount_type",
        ),
        {"schema": "billing"},
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    discount_type: Mapped[str | None] = mapped_column(String(10))
    discount_value: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="INR")
    max_uses: Mapped[int | None] = mapped_column(Integer)
    times_used: Mapped[int] = mapped_column(Integer, default=0)
    valid_from: Mapped[datetime | None] = mapped_column()
    valid_until: Mapped[datetime | None] = mapped_column()
    applicable_plans: Mapped[list] = mapped_column(ARRAY(PG_UUID(as_uuid=True)), default=list)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


# ---------------------------------------------------------------------------
# 30. SUBSCRIPTIONS
# ---------------------------------------------------------------------------
class Subscription(Base, TimestampMixin):
    __tablename__ = "subscriptions"
    __table_args__ = (
        CheckConstraint(
            "status IN ('active','paused','cancelled','expired','trialing','past_due')",
            name="ck_subscription_status",
        ),
        CheckConstraint(
            "billing_cycle IN ('monthly','yearly','lifetime')",
            name="ck_billing_cycle",
        ),
        Index("idx_subscriptions_user", "user_id"),
        Index("idx_subscriptions_status", "status"),
        Index("idx_subscriptions_period", "current_period_end"),
        {"schema": "billing"},
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("platform.users.id", ondelete="CASCADE"), nullable=False
    )
    plan_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("billing.subscription_plans.id"), nullable=False
    )
    product_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("catalog.products.id")
    )
    status: Mapped[str] = mapped_column(String(20), default="active")
    billing_cycle: Mapped[str | None] = mapped_column(String(10))
    current_period_start: Mapped[datetime | None] = mapped_column()
    current_period_end: Mapped[datetime | None] = mapped_column()
    trial_start: Mapped[datetime | None] = mapped_column()
    trial_end: Mapped[datetime | None] = mapped_column()
    cancelled_at: Mapped[datetime | None] = mapped_column()
    cancel_reason: Mapped[str | None] = mapped_column(Text)
    coupon_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("billing.coupons.id")
    )
    gateway: Mapped[str | None] = mapped_column(String(30))
    gateway_subscription_id: Mapped[str | None] = mapped_column(String(255))
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)

    plan = relationship("SubscriptionPlan", back_populates="subscriptions")
    invoices = relationship("Invoice", back_populates="subscription", cascade="all, delete-orphan")


# ---------------------------------------------------------------------------
# 32. INVOICES
# ---------------------------------------------------------------------------
class Invoice(Base):
    __tablename__ = "invoices"
    __table_args__ = (
        CheckConstraint(
            "status IN ('pending','paid','failed','refunded','void')",
            name="ck_invoice_status",
        ),
        Index("idx_invoices_user", "user_id"),
        Index("idx_invoices_sub", "subscription_id"),
        {"schema": "billing"},
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    subscription_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("billing.subscriptions.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("platform.users.id"), nullable=False
    )
    invoice_number: Mapped[str | None] = mapped_column(String(50), unique=True)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    tax_amount: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="INR")
    status: Mapped[str] = mapped_column(String(20), default="pending")
    due_date: Mapped[datetime | None] = mapped_column()
    paid_at: Mapped[datetime | None] = mapped_column()
    pdf_url: Mapped[str | None] = mapped_column(Text)
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    subscription = relationship("Subscription", back_populates="invoices")
    payments = relationship("Payment", back_populates="invoice", cascade="all, delete-orphan")


# ---------------------------------------------------------------------------
# 33. PAYMENTS
# ---------------------------------------------------------------------------
class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = (
        CheckConstraint(
            "status IN ('pending','completed','failed','refunded')",
            name="ck_payment_status",
        ),
        Index("idx_payments_user", "user_id"),
        Index("idx_payments_gateway", "gateway", "gateway_payment_id"),
        {"schema": "billing"},
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    invoice_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("billing.invoices.id")
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("platform.users.id"), nullable=False
    )
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="INR")
    gateway: Mapped[str] = mapped_column(String(30), nullable=False)
    gateway_payment_id: Mapped[str | None] = mapped_column(String(255))
    gateway_order_id: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(20), default="pending")
    payment_method: Mapped[str | None] = mapped_column(String(30))
    refund_amount: Mapped[float | None] = mapped_column(Numeric(10, 2))
    refund_reason: Mapped[str | None] = mapped_column(Text)
    refunded_at: Mapped[datetime | None] = mapped_column()
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    invoice = relationship("Invoice", back_populates="payments")


# ---------------------------------------------------------------------------
# 34. TRANSACTION HISTORY — Immutable ledger
# ---------------------------------------------------------------------------
class TransactionHistory(Base):
    __tablename__ = "transaction_history"
    __table_args__ = (
        CheckConstraint(
            "type IN ('charge','refund','credit','adjustment')",
            name="ck_txn_type",
        ),
        Index("idx_txn_user", "user_id"),
        Index("idx_txn_created", "created_at"),
        {"schema": "billing"},
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("platform.users.id"), nullable=False
    )
    type: Mapped[str] = mapped_column(String(20), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="INR")
    description: Mapped[str | None] = mapped_column(Text)
    reference_type: Mapped[str | None] = mapped_column(String(30))
    reference_id: Mapped[uuid.UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    balance_after: Mapped[float | None] = mapped_column(Numeric(10, 2))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
