from __future__ import annotations

from enum import Enum


class StrEnum(str, Enum):
    """Python 3.9-compatible replacement for enum.StrEnum (3.11+)."""

    def __str__(self) -> str:
        return self.value


class ContactStatus(StrEnum):
    PENDING = "pending"
    READ = "read"
    REPLIED = "replied"
    CLOSED = "closed"


class SubscriptionStatus(StrEnum):
    ACTIVE = "active"
    UNSUBSCRIBED = "unsubscribed"
    BOUNCED = "bounced"
    SPAM = "spam"


class ApplicationStatus(StrEnum):
    PENDING = "pending"
    REVIEWED = "reviewed"
    SHORTLISTED = "shortlisted"
    INTERVIEWED = "interviewed"
    OFFERED = "offered"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class QuoteStatus(StrEnum):
    PENDING = "pending"
    REVIEWED = "reviewed"
    QUOTED = "quoted"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"


class FeedbackCategory(StrEnum):
    GENERAL = "general"
    SERVICE = "service"
    SUPPORT = "support"
    WEBSITE = "website"
    BUG = "bug"
    FEATURE = "feature"
    OTHER = "other"


class ContentStatus(StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class BudgetRange(StrEnum):
    UNDER_10K = "under_10k"
    _10K_25K = "10k_25k"
    _25K_50K = "25k_50k"
    _50K_100K = "50k_100k"
    _100K_PLUS = "100k_plus"
    NOT_SURE = "not_sure"


class Timeline(StrEnum):
    IMMEDIATE = "immediate"
    _1_3_MONTHS = "1_3_months"
    _3_6_MONTHS = "3_6_months"
    _6_PLUS_MONTHS = "6_plus_months"
    NOT_SURE = "not_sure"
