from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from flows import router as flows_router

app = FastAPI(title="Bot Builder API", version="1.0.0")

# CORS для frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://62.113.104.172:5174", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(flows_router, prefix="/api", tags=["flows"])

@app.get("/")
async def root():
    return {"message": "Bot Builder API", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "ok"}