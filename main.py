from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.config.config import settings
from src.db.db import get_database
from src.routes import auth, onboarding, food
from src.middleware.middleware import request_logger_middleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await get_database()
    yield
    # (Optional) Shutdown logic goes here

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify: ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(onboarding.router, tags=["onboarding"])
app.include_router(food.router, tags=["food"])

# add middleware
app.middleware("http")(request_logger_middleware)

# Health check
@app.get("/health", tags=["system"])
async def health_check():
    return {"status": "ok", "app": settings.APP_NAME}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)