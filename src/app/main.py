from fastapi import FastAPI
from ..config.config import settings
from src.db.db import get_database
from ..routes import auth, onboarding, food
from src.middleware.middleware import request_logger_middleware

app = FastAPI(title=settings.APP_NAME)

# include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(onboarding.router, tags=["onboarding"])
app.include_router(food.router, tags=["food"])

# add middleware
app.middleware("http")(request_logger_middleware)

# Startup event (connect to DB)
@app.on_event("startup")
async def startup_event():
    await get_database()

# Health check
@app.get("/health", tags=["system"])
async def health_check():
    return {"status": "ok", "app": settings.APP_NAME}
