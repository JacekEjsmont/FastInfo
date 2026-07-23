from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pathlib import Path
from app.api.routes import articles, info_clusters
from app.web.routes import router as web_router
from dotenv import load_dotenv

print("Launching app!!!!!!!!")
load_dotenv()
app = FastAPI()

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
    return  RedirectResponse(url="/ui", status_code=307)
