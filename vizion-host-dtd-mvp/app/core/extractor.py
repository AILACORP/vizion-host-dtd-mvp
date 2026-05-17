import json

from app.prompts.loader import load_prompt
from app.schemas.extraction import ExtractionResult
from app.services.openai_service import run_json_prompt


async def extract_structure(text: str) -> ExtractionResult:
    system_prompt = load_prompt("extraction_json.md")
    raw = await run_json_prompt(system_prompt=system_prompt, user_prompt=text)
    data = json.loads(raw)
    return ExtractionResult(**data)
