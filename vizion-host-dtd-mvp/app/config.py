from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    openai_api_key: str
    telegram_bot_token: str
    telegram_webhook_secret: str | None = None
    app_env: str = "development"
    app_url: str | None = None
    whatsapp_token: str | None = None
    whatsapp_phone_number_id: str | None = None
    whatsapp_verify_token: str | None = None

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
