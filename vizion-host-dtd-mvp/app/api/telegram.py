from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.processor import process_text_message
from app.db.session import get_db
from app.services.telegram_service import send_telegram_message
from app.services.user_service import get_or_create_telegram_user

router = APIRouter()


@router.post("")
async def telegram_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.json()
    message = payload.get("message", {})
    chat = message.get("chat", {})

    if not chat:
        return {"ok": True, "ignored": True}

    telegram_id = str(chat.get("id"))
    name = chat.get("first_name") or chat.get("username")
    user = get_or_create_telegram_user(db, telegram_id=telegram_id, name=name)

    if "text" in message:
        text = message["text"]
        response = await process_text_message(db=db, user=user, text=text, source="telegram")
        await send_telegram_message(chat_id=telegram_id, text=response)
    elif "voice" in message:
        await send_telegram_message(chat_id=telegram_id, text="Audio recibido. La transcripción se activará en MVP v1.1.")
    else:
        await send_telegram_message(chat_id=telegram_id, text="Recibido. Por ahora el MVP procesa texto y próximamente audio.")

    return {"ok": True}
