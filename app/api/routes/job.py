from fastapi import APIRouter
from app.job_logic.add_articles_and_clusters_job import run_add_articles_and_clusters_job

router = APIRouter(prefix="/job")

@router.post("/run_add_articles_and_clusters")
def run_add_articles_and_clusters_call():
    run_add_articles_and_clusters_job()
    return {"status": "run_add_articles_and_clusters_job completed"}