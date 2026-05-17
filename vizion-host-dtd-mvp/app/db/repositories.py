from datetime import datetime, time
from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models import Entry, User


def get_or_create_user_by_telegram(db: Session, telegram_id: str, name: str | None = None) -> User:
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if user:
        return user

    user = User(telegram_id=telegram_id, name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_or_create_user_by_whatsapp(db: Session, whatsapp_id: str, name: str | None = None) -> User:
    user = db.query(User).filter(User.whatsapp_id == whatsapp_id).first()
    if user:
        return user

    user = User(whatsapp_id=whatsapp_id, name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_entry(db: Session, user_id: UUID, source: str, raw_input: str, extraction) -> Entry:
    entry = Entry(
        user_id=user_id,
        source=source,
        input_type=extraction.input_type,
        raw_input=raw_input,
        summary=extraction.summary,
        category=extraction.category,
        priority=extraction.priority,
        detected_tasks=[task.model_dump() for task in extraction.detected_tasks],
        detected_blockers=[blocker.model_dump() for blocker in extraction.detected_blockers],
        detected_topics=extraction.detected_topics,
        recommended_actions=extraction.recommended_actions,
        drift_signal=extraction.drift_signal,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def get_today_entries(db: Session, user_id: UUID) -> list[Entry]:
    today = datetime.combine(datetime.now().date(), time.min)
    return (
        db.query(Entry)
        .filter(Entry.user_id == user_id)
        .filter(Entry.created_at >= today)
        .order_by(Entry.created_at.asc())
        .all()
    )


def get_recent_entries(db: Session, user_id: UUID, limit: int = 50) -> list[Entry]:
    return (
        db.query(Entry)
        .filter(Entry.user_id == user_id)
        .order_by(Entry.created_at.desc())
        .limit(limit)
        .all()
    )
