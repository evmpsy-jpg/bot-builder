from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import logging
import sys
import os

from app.core import settings, init_db
from app.api.v1 import auth, bots, flows
from app.api.v1 import flows_import

# Создание логов директории
os.makedirs(settings.LOG_DIR, exist_ok=True)

# Настройка логирования
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(f'{settings.LOG_DIR}/app.log')
    ]
)

logger = logging.getLogger(__name__)

# Создание FastAPI приложения
app = FastAPI(
    title=settings.APP_NAME,
    description="Production-ready Bot Builder API with Flows, Payments, and Analytics",
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json",
)

# Middleware для CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Middleware для доверенных хостов
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]
)

# Подключаем роутеры
app.include_router(auth.router, prefix="/api/v1")
app.include_router(bots.router, prefix="/api/v1")
app.include_router(flows.router, prefix="/api/v1")
app.include_router(flows_import.router, prefix="/api/v1", tags=["flows-import"])

# Инициализация БД при запуске
@app.on_event("startup")
async def startup_event():
    """Инициализация при запуске приложения"""
    logger.info(f"🚀 Starting {settings.APP_NAME}")
    logger.info(f"📍 Environment: {settings.ENVIRONMENT}")
    logger.info(f"📊 Database: {settings.DATABASE_URL}")
    
    try:
        init_db()
        logger.info("✅ Database initialized successfully")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Очистка при остановке приложения"""
    logger.info(f"🛑 Shutting down {settings.APP_NAME}")

# Маршруты здоровья
@app.get("/health")
async def health():
    """Проверка здоровья приложения"""
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT,
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    """Корневой маршрут"""
    return {
        "message": "Welcome to Bot Builder API",
        "docs": "/api/v1/docs",
        "health": "/health",
        "version": "1.0.0"
    }

# Обработка исключений
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Глобальная обработка исключений"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "error": str(exc) if settings.DEBUG else "An error occurred"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
