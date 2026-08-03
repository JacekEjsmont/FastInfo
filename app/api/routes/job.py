from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.job_logic.job_logics import run_add_articles_and_clusters_job, run_delete_6_days_old_call_job

router = APIRouter(prefix="/job")

@router.post("/run_add_articles_and_clusters")
def run_add_articles_and_clusters_call():
    run_add_articles_and_clusters_job()
    return {"status": "run_add_articles_and_clusters_job completed"}

@router.delete("/run_delete_6_days_old")
def run_delete_6_days_old_call(db: Session = Depends(get_db)):
    number_of_articles_deleted = run_delete_6_days_old_call_job(db)
    return {"status": f"run_delete_6_days_old completed. Deleted {number_of_articles_deleted} articles"}
