import uuid

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    telegram_id = Column(Text, unique=True, nullable=True)
    whatsapp_id = Column(Text, unique=True, nullable=True)
    name = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class Entry(Base):
    __tablename__ = "entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    source = Column(Text, nullable=False)
    input_type = Column(Text, nullable=False)
    raw_input = Column(Text, nullable=True)
    transcript = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    category = Column(Text, nullable=True)
    priority = Column(Text, nullable=True)
    detected_tasks = Column(JSON, default=list)
    detected_blockers = Column(JSON, default=list)
    detected_topics = Column(JSON, default=list)
    recommended_actions = Column(JSON, default=list)
    drift_signal = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class DailySummary(Base):
    __tablename__ = "daily_summaries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    summary = Column(Text, nullable=False)
    active_topics = Column(JSON, default=list)
    completed_items = Column(JSON, default=list)
    pending_items = Column(JSON, default=list)
    blockers = Column(JSON, default=list)
    next_actions = Column(JSON, default=list)
    drift_level = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (UniqueConstraint("user_id", "date", name="uq_user_daily_summary"),)


class Pattern(Base):
    __tablename__ = "patterns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    pattern_type = Column(Text, nullable=False)
    topic = Column(Text, nullable=True)
    frequency = Column(Integer, default=1)
    severity = Column(Text, nullable=True)
    evidence = Column(JSON, default=list)
    first_seen = Column(DateTime, server_default=func.now())
    last_seen = Column(DateTime, server_default=func.now())
