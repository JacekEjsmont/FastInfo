from fastapi import APIRouter, Depends
from app.ingestion.ingestion_service import ingest_articles
from app.db import query
from sqlalchemy.orm import Session
from app.db.database import get_db

router = APIRouter(prefix="/articles")

@router.post("/ingest")
def ingest(db: Session = Depends(get_db)):
    ingest_articles(db=db)
    return {"status": "ingested"}

@router.post("/ingest_local")
def ingest_local(db: Session = Depends(get_db)):
    ingest_articles(local=True, db=db)
    return {"status": "ingested"}

@router.post("/update_publish_status")
def update_publish_status(db: Session = Depends(get_db)):
    number_of_status_updated = query.update_article_publish_status(db)
    return {"status": "article publish status updated for " + str(number_of_status_updated)}


@router.get("/all_articles")
def all_articles(db: Session = Depends(get_db)):
    return query.get_all_articles(db)

@router.get("/article")
def root(article_id: str, db: Session = Depends(get_db)):
    return query.get_article_by_id(article_id, db)
