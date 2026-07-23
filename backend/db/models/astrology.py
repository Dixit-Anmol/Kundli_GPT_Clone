"""
Module 4 — Astrology Models.

Tables: astro_profiles, astro_birth_details, astro_charts, astro_planet_positions,
        astro_houses, astro_yogas, astro_doshas, astro_dashas, astro_divisional_charts
Schema: astrology
"""

import uuid
from datetime import date, datetime, time

from sqlalchemy import (
    Boolean, CheckConstraint, Date, Float, ForeignKey, Index,
    Integer, SmallInteger, String, Text, Time,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base, TimestampMixin, SoftDeleteMixin, new_uuid


# ---------------------------------------------------------------------------
# 15. ASTRO PROFILES — One per person (self, spouse, child, friend)
# ---------------------------------------------------------------------------
class AstroProfile(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "astro_profiles"
    __table_args__ = (
        CheckConstraint(
            "relationship IN ('self','spouse','child','parent','friend','other')",
            name="ck_astro_profile_rel",
        ),
        Index("idx_astro_profiles_user", "user_id"),
        {"schema": "astrology"},
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("platform.users.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    relationship_type: Mapped[str] = mapped_column("relationship", String(30), default="self")
    gender: Mapped[str | None] = mapped_column(String(10))
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)

    birth_details = relationship("AstroBirthDetails", back_populates="profile", uselist=False, cascade="all, delete-orphan")
    charts = relationship("AstroChart", back_populates="profile", cascade="all, delete-orphan")


# ---------------------------------------------------------------------------
# 16. BIRTH DETAILS
# ---------------------------------------------------------------------------
class AstroBirthDetails(Base, TimestampMixin):
    __tablename__ = "astro_birth_details"
    __table_args__ = (
        CheckConstraint(
            "mode IN ('exact','partial','prashna')",
            name="ck_birth_mode",
        ),
        {"schema": "astrology"},
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    profile_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("astrology.astro_profiles.id", ondelete="CASCADE"),
        unique=True, nullable=False,
    )
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    time_of_birth: Mapped[time | None] = mapped_column(Time)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    timezone_offset: Mapped[float] = mapped_column(Float, default=5.5)
    place_name: Mapped[str | None] = mapped_column(String(255))
    mode: Mapped[str] = mapped_column(String(20), default="exact")
    time_slot: Mapped[str | None] = mapped_column(String(30))
    prashna_question: Mapped[str | None] = mapped_column(Text)
    prashna_category: Mapped[str | None] = mapped_column(String(50))

    profile = relationship("AstroProfile", back_populates="birth_details")


# ---------------------------------------------------------------------------
# 17. ASTRO CHARTS — Versioned chart calculations
# ---------------------------------------------------------------------------
class AstroChart(Base):
    __tablename__ = "astro_charts"
    __table_args__ = (
        CheckConstraint(
            "chart_type IN ('natal','transit','progressed','solar_return','prashna')",
            name="ck_chart_type",
        ),
        Index("idx_charts_profile", "profile_id"),
        Index("idx_charts_type", "chart_type"),
        Index("idx_charts_computed", "computed_at"),
        {"schema": "astrology"},
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    profile_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("astrology.astro_profiles.id", ondelete="CASCADE"), nullable=False
    )
    chart_type: Mapped[str] = mapped_column(String(30), default="natal")
    version: Mapped[int] = mapped_column(Integer, default=1)
    ayanamsa: Mapped[float | None] = mapped_column(Float)
    ascendant_sign: Mapped[str | None] = mapped_column(String(20))
    ascendant_longitude: Mapped[float | None] = mapped_column(Float)
    moon_sign: Mapped[str | None] = mapped_column(String(20))
    nakshatra: Mapped[str | None] = mapped_column(String(30))
    nakshatra_pada: Mapped[int | None] = mapped_column(SmallInteger)
    raw_data: Mapped[dict] = mapped_column(JSONB, nullable=False)
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)
    computed_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    profile = relationship("AstroProfile", back_populates="charts")
    planet_positions = relationship("AstroPlanetPosition", back_populates="chart", cascade="all, delete-orphan")
    houses = relationship("AstroHouse", back_populates="chart", cascade="all, delete-orphan")
    yogas = relationship("AstroYoga", back_populates="chart", cascade="all, delete-orphan")
    doshas = relationship("AstroDosha", back_populates="chart", cascade="all, delete-orphan")
    dashas = relationship("AstroDasha", back_populates="chart", cascade="all, delete-orphan")
    divisional_charts = relationship("AstroDivisionalChart", back_populates="chart", cascade="all, delete-orphan")


# ---------------------------------------------------------------------------
# 18. PLANET POSITIONS
# ---------------------------------------------------------------------------
class AstroPlanetPosition(Base):
    __tablename__ = "astro_planet_positions"
    __table_args__ = (
        Index("idx_planet_pos_chart", "chart_id"),
        Index("idx_planet_pos_planet", "planet"),
        {"schema": "astrology"},
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    chart_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("astrology.astro_charts.id", ondelete="CASCADE"), nullable=False
    )
    planet: Mapped[str] = mapped_column(String(20), nullable=False)
    planet_sanskrit: Mapped[str | None] = mapped_column(String(30))
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    sign: Mapped[str] = mapped_column(String(20), nullable=False)
    degree: Mapped[float | None] = mapped_column(Float)
    house: Mapped[int | None] = mapped_column(SmallInteger)
    dignity: Mapped[str | None] = mapped_column(String(30))
    is_retrograde: Mapped[bool] = mapped_column(Boolean, default=False)
    is_combust: Mapped[bool] = mapped_column(Boolean, default=False)
    nakshatra_name: Mapped[str | None] = mapped_column(String(30))
    nakshatra_lord: Mapped[str | None] = mapped_column(String(20))
    nakshatra_pada: Mapped[int | None] = mapped_column(SmallInteger)
    speed: Mapped[float | None] = mapped_column(Float)

    chart = relationship("AstroChart", back_populates="planet_positions")


# ---------------------------------------------------------------------------
# 19. HOUSES
# ---------------------------------------------------------------------------
class AstroHouse(Base):
    __tablename__ = "astro_houses"
    __table_args__ = (
        Index("idx_houses_chart", "chart_id"),
        {"schema": "astrology"},
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    chart_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("astrology.astro_charts.id", ondelete="CASCADE"), nullable=False
    )
    house_number: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    sign: Mapped[str] = mapped_column(String(20), nullable=False)
    lord: Mapped[str | None] = mapped_column(String(20))
    cusp_longitude: Mapped[float | None] = mapped_column(Float)
    signification: Mapped[str | None] = mapped_column(Text)

    chart = relationship("AstroChart", back_populates="houses")


# ---------------------------------------------------------------------------
# 20. YOGAS
# ---------------------------------------------------------------------------
class AstroYoga(Base):
    __tablename__ = "astro_yogas"
    __table_args__ = (
        Index("idx_yogas_chart", "chart_id"),
        {"schema": "astrology"},
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    chart_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("astrology.astro_charts.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str | None] = mapped_column(String(30))
    involved_planets: Mapped[str | None] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    strength: Mapped[str | None] = mapped_column(String(20))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    chart = relationship("AstroChart", back_populates="yogas")


# ---------------------------------------------------------------------------
# 21. DOSHAS
# ---------------------------------------------------------------------------
class AstroDosha(Base):
    __tablename__ = "astro_doshas"
    __table_args__ = (
        Index("idx_doshas_chart", "chart_id"),
        {"schema": "astrology"},
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    chart_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("astrology.astro_charts.id", ondelete="CASCADE"), nullable=False
    )
    dosha_type: Mapped[str] = mapped_column(String(30), nullable=False)
    is_present: Mapped[bool] = mapped_column(Boolean, default=False)
    severity: Mapped[str | None] = mapped_column(String(20))
    details: Mapped[dict] = mapped_column(JSONB, default=dict)

    chart = relationship("AstroChart", back_populates="doshas")


# ---------------------------------------------------------------------------
# 22. DASHAS
# ---------------------------------------------------------------------------
class AstroDasha(Base):
    __tablename__ = "astro_dashas"
    __table_args__ = (
        CheckConstraint(
            "level IN ('mahadasha','antardasha','pratyantardasha')",
            name="ck_dasha_level",
        ),
        Index("idx_dashas_chart", "chart_id"),
        Index("idx_dashas_dates", "start_date", "end_date"),
        {"schema": "astrology"},
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    chart_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("astrology.astro_charts.id", ondelete="CASCADE"), nullable=False
    )
    dasha_system: Mapped[str] = mapped_column(String(30), default="vimshottari")
    level: Mapped[str] = mapped_column(String(20), nullable=False)
    planet: Mapped[str] = mapped_column(String(20), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("astrology.astro_dashas.id")
    )
    sequence_order: Mapped[int | None] = mapped_column(SmallInteger)

    chart = relationship("AstroChart", back_populates="dashas")
    parent = relationship("AstroDasha", remote_side="AstroDasha.id")


# ---------------------------------------------------------------------------
# 23. DIVISIONAL CHARTS
# ---------------------------------------------------------------------------
class AstroDivisionalChart(Base):
    __tablename__ = "astro_divisional_charts"
    __table_args__ = (
        Index("idx_div_charts_chart", "chart_id"),
        {"schema": "astrology"},
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=new_uuid)
    chart_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("astrology.astro_charts.id", ondelete="CASCADE"), nullable=False
    )
    division: Mapped[str] = mapped_column(String(10), nullable=False)
    name: Mapped[str | None] = mapped_column(String(50))
    raw_data: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    chart = relationship("AstroChart", back_populates="divisional_charts")
