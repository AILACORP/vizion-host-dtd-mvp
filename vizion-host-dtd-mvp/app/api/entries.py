from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.repositories import get_recent_entries
from app.db.session import get_db

router = APIRouter()


@router.get("/{user_id}/recent")
def recent_entries(user_id: UUID, db: Session = Depends(get_db)):
    entries = get_recent_entries(db, user_id=user_id, limit=20)
    return {
        "items": [
            {
                "id": str(entry.id),
                "raw_input": entry.raw_input,
                "summary": entry.summary,
                "priority": entry.priority,
                "created_at": entry.created_at.isoformat() if entry.created_at else None,
            }
            for entry in entries
        ]
    }
