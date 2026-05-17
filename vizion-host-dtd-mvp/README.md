# VIZION HOST + Descarga Tu Día MVP

MVP Telegram + WhatsApp para capturar pensamientos, tareas, bloqueos y descargas diarias, convertirlas en estructura operacional y generar continuidad.

## Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- OpenAI API
- Telegram Bot API
- WhatsApp Cloud API

## Setup local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
docker compose up -d
uvicorn app.main:app --reload
```

Probar:

```bash
curl http://localhost:8000/health
```

## Telegram webhook local con ngrok

```bash
ngrok http 8000
curl -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/setWebhook" \
  -d "url=https://YOUR-NGROK-URL/webhooks/telegram"
```

## WhatsApp Cloud API webhook

Webhook URL:

```txt
https://YOUR-DOMAIN/webhooks/whatsapp
```

Verify token:

```txt
WHATSAPP_VERIFY_TOKEN
```

## Commands

- `/start`
- `/resumen`

## MVP v1 Scope

Incluye:

- captura por texto,
- extracción JSON,
- memoria PostgreSQL,
- respuesta operacional,
- resumen diario manual,
- Telegram webhook,
- WhatsApp webhook.

Pendiente para v1.1:

- audio transcription,
- pattern endpoint,
- auth dashboard,
- billing.
