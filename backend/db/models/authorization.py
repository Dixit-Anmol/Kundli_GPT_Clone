"""
Module 2 — Authorization Models (Enterprise RBAC).

Tables: roles, permissions, role_permissions, user_roles
Schema: authz
"""

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean, CheckConstraint, ForeignKey, Index, String, Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base, new_uuid


# ---------------------------------------------------------------------------
# 7. ROLES
# ---------------------------------------------------------------------------
class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {"schema": "authz"}

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    is_system: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    permissions = relationship("RolePermission", back_populates="role", cascade="all, delete-orphan")
    users = relationship("UserRole", back_populates="role", cascade="all, delete-orphan")


# ---------------------------------------------------------------------------
# 8. PERMISSIONS
# ---------------------------------------------------------------------------
class Permission(Base):
    __tablename__ = "permissions"
    __table_args__ = (
        CheckConstraint(
            "action IN ('create','read','update','delete','execute','manage')",
            name="ck_permission_action",
        ),
        {"schema": "authz"},
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    codename: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    resource: Mapped[str | None] = mapped_column(String(50))
    action: Mapped[str | None] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


# ---------------------------------------------------------------------------
# 9. ROLE → PERMISSION mapping
# ---------------------------------------------------------------------------
class RolePermission(Base):
    __tablename__ = "role_permissions"
    __table_args__ = {"schema": "authz"}

    role_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("authz.roles.id", ondelete="CASCADE"),
        primary_key=True,
    )
    permission_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("authz.permissions.id", ondelete="CASCADE"),
        primary_key=True,
    )

    role = relationship("Role", back_populates="permissions")
    permission = relationship("Permission")


# ---------------------------------------------------------------------------
# 10. USER → ROLE mapping
# ---------------------------------------------------------------------------
class UserRole(Base):
    __tablename__ = "user_roles"
    __table_args__ = (
        Index("idx_user_roles_user", "user_id"),
        {"schema": "authz"},
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("platform.users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    role_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("authz.roles.id", ondelete="CASCADE"),
        primary_key=True,
    )
    granted_by: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("platform.users.id")
    )
    granted_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    expires_at: Mapped[datetime | None] = mapped_column()

    role = relationship("Role", back_populates="users")
