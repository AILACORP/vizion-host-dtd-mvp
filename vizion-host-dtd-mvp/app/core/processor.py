from sqlalchemy.orm import Session

from app.core.extractor import extract_structure
from app.core.summarizer import generate_daily_summary
from app.db.models import User
from app.db.repositories import create_entry, get_today_entries


async def process_text_message(db: Session, user: User, text: str, source: str) -> str:
    command = text.strip().lower()

    if not command:
        return "Recibido vacío. Mándame un pendiente, idea, problema o descarga completa."

    if command == "/start":
        return onboarding_message()

    if command in ["/resumen", "resumen", "cierre"]:
        entries = get_today_entries(db, user.id)
        return await generate_daily_summary(entries=entries)

    try:
        extraction = await extract_structure(text=text)
        create_entry(db=db, user_id=user.id, source=source, raw_input=text, extraction=extraction)
        return extraction.response_to_user
    except Exception:
        return "No pude procesar completamente la descarga. Intenta resumirlo un poco más o vuelve a intentarlo."


def onboarding_message() -> str:
    return """
Bienvenido a VIZION HOST.

Este sistema te ayuda a descargar, ordenar y dar continuidad a tu día.

Puedes enviarme:
- pendientes,
- ideas,
- audios,
- problemas,
- tareas,
- o una descarga completa de lo que traes en mente.

Yo lo convierto en claridad, prioridades, acciones, resumen diario y continuidad.

Para empezar:
¿Qué necesitas descargar hoy?
""".strip()
