from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.pool import StaticPool
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Генерируем DATABASE_URL
DATABASE_URL = settings.DATABASE_URL

# Определяем параметры движка в зависимости от БД
if "sqlite" in DATABASE_URL:
    # SQLite конфигурация
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=settings.DEBUG
    )
else:
    # PostgreSQL конфигурация
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        echo=settings.DEBUG
    )

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base для моделей
Base = declarative_base()

def get_db() -> Session:
    """Dependency для получения сессии БД"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Инициализация БД - создание всех таблиц"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully")
    except Exception as e:
        logger.error(f"❌ Database initialization error: {str(e)}")
        raise

def drop_db():
    """Удаление всех таблиц (только для development!)"""
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("✅ Database tables dropped")
    except Exception as e:
        logger.error(f"❌ Database drop error: {str(e)}")
        raise
