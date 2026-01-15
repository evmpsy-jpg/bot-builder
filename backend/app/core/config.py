from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    """Глобальные настройки приложения"""
    
    # Базовые настройки
    APP_NAME: str = "Bot Builder API"
    APP_URL: str = os.getenv("APP_URL", "http://localhost:8000")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR: str = os.getenv("LOG_DIR", "logs")
    
    # База данных
    DB_NAME: str = os.getenv("DB_NAME", "bot_builder.db")
    DB_USER: str = os.getenv("DB_USER", "sqlite")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_HOST: str = os.getenv("DB_HOST", "")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    
    # Telegram
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_WEBHOOK_URL: str = os.getenv("TELEGRAM_WEBHOOK_URL", "")
    
    # JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    # Integrации (опционально)
    PRODAMUS_API_KEY: str = os.getenv("PRODAMUS_API_KEY", "")
    STRIPE_API_KEY: str = os.getenv("STRIPE_API_KEY", "")
    STRIPE_WEBHOOK_SECRET: str = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    
    # Redis (опционально)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Email (опционально)
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM_EMAIL: str = os.getenv("SMTP_FROM_EMAIL", "noreply@yourdomain.com")
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Разрешить extra поля из .env
    
    @property
    def CORS_ORIGINS(self) -> list:
        """Получить CORS origins из .env"""
        cors_str = os.getenv("CORS_ORIGINS", "http://localhost,http://localhost:3000,http://localhost:5173")
        return [origin.strip() for origin in cors_str.split(",")]
    
    @property
    def DATABASE_URL(self) -> str:
        """Генерируем URL базы данных в зависимости от типа"""
        if "sqlite" in self.DB_NAME or self.DB_HOST == "":
            # SQLite
            return f"sqlite:///{self.DB_NAME}"
        else:
            # PostgreSQL
            return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

@lru_cache()
def get_settings() -> Settings:
    """Получить кешированные настройки"""
    return Settings()

# Экспортируем глобальный объект settings
settings = get_settings()
