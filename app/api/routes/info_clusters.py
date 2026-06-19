from fastapi import APIRouter, Depends
from app.infocluster.info_cluster_service import refresh_info_clusters
from app.ai.clustering import cluster_by_similarity
from app.ai import vector_store
from app.db import query
from sqlalchemy.orm import Session
from app.db.database import get_db

router = APIRouter(prefix="/infos")

@router.post("/process_info_clusters")
def process_info_clusters():
    refresh_info_clusters()
    return {"status": "info clusters processed"}

@router.get("/all_info_clusters")
def all_info_clusters(db: Session = Depends(get_db)):
    return query.get_all_info_clusters(db)

@router.get("/info_cluster")
def info_cluster(info_cluster_id: str, db: Session = Depends(get_db)):
    return query.get_info_cluster_by_id(info_cluster_id, db)

@router.get("/show_possible_clusters")
def show_possible_clusters():
    articles_embeddings = vector_store.get_all_embeddings()
    return cluster_by_similarity(articles_embeddings["embeddings"].tolist(), articles_embeddings["ids"], 0.35)

@router.get("/show_possible_clusters_by_tags")
def show_possible_clusters_by_tags():
    articles_embeddings = vector_store.get_all_embeddings_by_tags()
    return cluster_by_similarity(articles_embeddings["embeddings"].tolist(), articles_embeddings["ids"], 0.15)