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

# @router.delete("/all_articles")
# def all_articles():
#     # return query.delete_everything()
#     return query.delete_where_claims_empty()
#
# @router.get("/all_embeddings") # /articles/all_embeddings  TRZEBA PEWNIE PODZIELAC ROUTERY
# def all_embeddings():
#     articles_embeddings = vector_store.get_all_embeddings()
#     # return articles_embeddings.get("embeddings").tolist()
#     return articles_embeddings.get("ids")
#
# @router.get("/all_embeddings_by_tags") # /articles/all_embeddings  TRZEBA PEWNIE PODZIELAC ROUTERY
# def all_embeddings():
#     articles_embeddings = vector_store.get_all_embeddings_by_tags()
#     # return articles_embeddings.get("embeddings").tolist()
#     return articles_embeddings.get("ids")
#
# @router.post("/embed")
# def embed():
#     vector_store.store_embeddings()
#     return {"status": "embedded"}
#
# @router.get("/all_cluster")
# def get_all_cluster():
#     articles_embeddings = vector_store.get_all_embeddings()
#     return cluster_by_similarity(articles_embeddings["embeddings"].tolist(), articles_embeddings["ids"])
#
# @router.get("/all_cluster_by_tags")
# def get_all_cluster_by_tags():
#     articles_embeddings = vector_store.get_all_embeddings_by_tags()
#     return cluster_by_similarity(articles_embeddings["embeddings"].tolist(), articles_embeddings["ids"], 0.15)