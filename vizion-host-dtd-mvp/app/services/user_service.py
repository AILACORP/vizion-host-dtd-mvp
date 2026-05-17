from sqlalchemy.orm import Session

from app.db.models import User
from app.db.repositories import get_or_create_user_by_telegram, get_or_create_user_by_whatsapp


def get_or_create_telegram_user(db: Session, telegram_id: str, name: str | None = None) -> User:
    return get_or_create_user_by_telegram(db=db, telegram_id=telegram_id, name=name)


def get_or_create_whatsapp_user(db: Session, whatsapp_id: str, name: str | None = None) -> User:
    return get_or_create_user_by_whatsapp(db=db, whatsapp_id=whatsapp_id, name=name)
