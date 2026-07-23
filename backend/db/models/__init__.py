"""
Exposes all SQLAlchemy ORM models for Alembic discovery.
"""

from db.base import Base
from db.models.identity import User, AuthProvider, UserProfile, UserPreference, UserDevice, UserSession
from db.models.authorization import Role, Permission, RolePermission, UserRole
from db.models.products import Product, UserProduct, ProductFeature, FeatureFlag
from db.models.astrology import (
    AstroProfile, AstroBirthDetails, AstroChart, AstroPlanetPosition,
    AstroHouse, AstroYoga, AstroDosha, AstroDasha, AstroDivisionalChart
)
from db.models.ai_chat import ChatSession, ChatMessage, ChatAttachment, ChatFeedback
from db.models.reports import AIReport
from db.models.billing import SubscriptionPlan, Coupon, Subscription, Invoice, Payment, TransactionHistory
from db.models.storage import FileAsset
from db.models.notifications import Notification, NotificationPreference
from db.models.analytics import UserAnalyticsEvent, SystemMetric, AIAnalytics, UserDailyUsage
from db.models.audit import AuditLog
from db.models.system import APIKey, Webhook, BackgroundJob, SystemSetting, RateLimit

__all__ = [
    "Base",
    "User",
    "AuthProvider",
    "UserProfile",
    "UserPreference",
    "UserDevice",
    "UserSession",
    "Role",
    "Permission",
    "RolePermission",
    "UserRole",
    "Product",
    "UserProduct",
    "ProductFeature",
    "FeatureFlag",
    "AstroProfile",
    "AstroBirthDetails",
    "AstroChart",
    "AstroPlanetPosition",
    "AstroHouse",
    "AstroYoga",
    "AstroDosha",
    "AstroDasha",
    "AstroDivisionalChart",
    "ChatSession",
    "ChatMessage",
    "ChatAttachment",
    "ChatFeedback",
    "AIReport",
    "SubscriptionPlan",
    "Coupon",
    "Subscription",
    "Invoice",
    "Payment",
    "TransactionHistory",
    "FileAsset",
    "Notification",
    "NotificationPreference",
    "UserAnalyticsEvent",
    "SystemMetric",
    "AIAnalytics",
    "UserDailyUsage",
    "AuditLog",
    "APIKey",
    "Webhook",
    "BackgroundJob",
    "SystemSetting",
    "RateLimit",
]
