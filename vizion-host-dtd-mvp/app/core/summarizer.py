from app.prompts.loader import load_prompt
from app.services.openai_service import run_text_prompt


async def generate_daily_summary(entries) -> str:
    if not entries:
        return "Todavía no hay suficientes entradas registradas hoy para generar un resumen útil."

    prompt = load_prompt("daily_summary.md")
    user_prompt = "\n\n".join(
        [
            f"Entrada: {entry.raw_input}\n"
            f"Resumen: {entry.summary}\n"
            f"Tareas: {entry.detected_tasks}\n"
            f"Bloqueos: {entry.detected_blockers}\n"
            f"Prioridad: {entry.priority}"
            for entry in entries
        ]
    )
    return await run_text_prompt(system_prompt=prompt, user_prompt=user_prompt)
