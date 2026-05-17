from app.prompts.loader import load_prompt
from app.services.openai_service import run_text_prompt


async def detect_patterns(entries) -> str:
    if len(entries) < 5:
        return "No hay suficientes datos para detectar patrones confiables todavía."

    prompt = load_prompt("patterns.md")
    user_prompt = "\n\n".join(
        [
            f"Entrada: {entry.raw_input}\n"
            f"Temas: {entry.detected_topics}\n"
            f"Bloqueos: {entry.detected_blockers}\n"
            f"Drift: {entry.drift_signal}"
            for entry in entries
        ]
    )
    return await run_text_prompt(system_prompt=prompt, user_prompt=user_prompt)
