from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.api.routes import articles, info_clusters, embed, job
from app.web.routes import router as web_router
from app.db.database import engine, Base
from app.db import models

print("Launching app!!!!!!!!")
app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(articles.router)
app.include_router(info_clusters.router)
app.include_router(embed.router)
app.include_router(job.router)
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


