from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parent


def load_prompt(filename: str) -> str:
    path = PROMPTS_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {filename}")
    return path.read_text(encoding="utf-8")
