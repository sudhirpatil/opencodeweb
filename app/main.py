from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.api.analyze import router as analyze_router
from app.api.apply import router as apply_router
from app.api.files import router as files_router
from app.config import settings

app = FastAPI(title="PySpark Code Review Agent", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze_router)
app.include_router(apply_router)
app.include_router(files_router)

app.mount("/", StaticFiles(directory=settings.static_dir, html=True), name="static")
