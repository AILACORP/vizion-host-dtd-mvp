from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.config import settings
from app.core.processor import process_text_message
from app.db.session import get_db
from app.services.user_service import get_or_create_whatsapp_user
from app.services.whatsapp_service import send_whatsapp_message

router = APIRouter()


@router.get("")
async def verify_webhook(request: Request):
    params = request.query_params
    if (
        params.get("hub.mode") == "subscribe"
        and params.get("hub.verify_token") == settings.whatsapp_verify_token
    ):
        return int(params.get("hub.challenge", "0"))
    return {"error": "verification_failed"}


@router.post("")
async def whatsapp_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.json()

    try:
        value = payload["entry"][0]["changes"][0]["value"]
        messages = value.get("messages", [])
        if not messages:
            return {"ok": True, "ignored": True}

        message = messages[0]
        user_phone = message["from"]

        if message.get("type") != "text":
            await send_whatsapp_message(to=user_phone, text="Recibido. Por ahora el MVP procesa texto y próximamente audio.")
            return {"ok": True}

        text = message["text"]["body"]
        user = get_or_create_whatsapp_user(db, whatsapp_id=user_phone)
        response = await process_text_message(db=db, user=user, text=text, source="whatsapp")
        await send_whatsapp_message(to=user_phone, text=response)
    except Exception:
        # Meta expects 200 to avoid retries. Add structured logging before production scale.
        pass

    return {"ok": True}
