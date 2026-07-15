from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.api.routes import articles, info_clusters
from app.web.routes import router as web_router
from app.db.database import engine, Base
from dotenv import load_dotenv
from app.db import models
import time

print("Launching app!!!!!!!!")
load_dotenv()
app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(articles.router)
app.include_router(info_clusters.router)
app.include_router(web_router)

static_dir = Path(__file__).resolve().parent / "web" / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

logo_path = Path(__file__).resolve().parent.parent / "logo.png"


@app.get("/logo.png")
def logo():
    return FileResponse(logo_path)

@app.get("/")
def root():
    return {"status": "ok"}

@app.on_event("startup")
def create_tables_with_retry() -> None:
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            Base.metadata.create_all(bind=engine)
            return
        except Exception as exc:
            last_error = exc
            if attempt < 2:
                time.sleep(2 ** attempt)
    if last_error is not None:
        raise last_error


