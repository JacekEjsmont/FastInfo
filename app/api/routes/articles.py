from fastapi import APIRouter, Depends
from app.ingestion.ingestion_service import ingest_articles
from app.db import query
from sqlalchemy.orm import Session
from app.db.database import get_db

router = APIRouter(prefix="/articles")

@router.post("/ingest")
def ingest():
    ingest_articles()
    return {"status": "ingested"}

@router.get("/all_articles")
def all_articles(db: Session = Depends(get_db)):
    return query.get_all_articles(db)

@router.get("/article")
def root(article_id: str, db: Session = Depends(get_db)):
    return query.get_article_by_id(article_id, db)
