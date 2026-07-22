from fastapi import FastAPI
from app.api.upload_api import router as upload_router
from app.api.extract_api import router as extract_router
#from app.api.user_api import router
from app.api.stats_api import router as stats_router
from app.api.search_api import router as search_router
from app.api.search_api import router as search_router
from app.api.chunks_api import router as chunks_router
from app.api.ask_api import router as ask_router
from app.api.documents_api import router as documents_router
from app.api.statistics_api import router as statistics_router
from app.api.source_api import router as source_router
from app.api.history_api import router as history_router
from app.api.question_search_api import router as question_search
from app.api.health_api import router as health
from app.api.download_api import router as download_router
from app.api.analytics_api import (
    router as analytics_router
)

from app.api.dashboard_api import router as dashboard_router

from app.api.recent_documents_api import (
    router as recent_documents_router
)

from app.api.filetype_statistics_api import (
    router as filetype_router
)

from app.api.subject_statistics_api import (
    router as subject_statistics_router
)

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.grouped_history_api import (
    router as grouped_history_router
)
from app.api.document_search_api import (
    router as document_search_router
)
from app.database.connection import engine
from app.database.models import Base

# Import models so SQLAlchemy registers every table
import app.database.models
from pathlib import Path
from fastapi.staticfiles import StaticFiles



Base.metadata.create_all(bind=engine)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(upload_router)
app.include_router(extract_router)
app.include_router(search_router)
app.include_router(chunks_router)
#app.include_router(chat_router)
app.include_router(ask_router)
#app.include_router(router)
app.include_router(documents_router)
app.include_router(
    document_search_router
)
app.include_router(statistics_router)
app.include_router(source_router)
app.include_router(dashboard_router)
app.include_router(
    analytics_router
)
app.include_router(recent_documents_router)

app.include_router(filetype_router)

app.include_router(subject_statistics_router)
app.include_router(history_router)
app.include_router(question_search)
app.include_router(stats_router)
app.include_router(download_router)
app.include_router(health)
app.include_router(
    grouped_history_router
)
app.include_router(
    document_search_router
)

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

UPLOADS_DIR = BASE_DIR / "uploads"

print("Serving uploads from:", UPLOADS_DIR)
app.mount(
    "/uploads",
    StaticFiles(directory=str(UPLOADS_DIR)),
    name="uploads"
)
@app.post("/")
def home():
    return {"message":"Project Running"}