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
def show_possible_clusters(db: Session = Depends(get_db)):
    articles_embeddings = vector_store.get_all_embeddings()
    info_clusters_first_run = cluster_by_similarity(list(articles_embeddings.values()), list(articles_embeddings.keys()))
    info_clusters = cluster_by_similarity(list(articles_embeddings.values()), list(articles_embeddings.keys()), clusters=info_clusters_first_run)

    only_clusters = [cluster for cluster in info_clusters if len(cluster) >= 2]
    clusters_transformed = []
    for cluster in only_clusters:
        article_id_to_article = {}
        for article in cluster:
            article_id = article[0]
            article_id_to_article[article_id] = query.get_article_by_id(int(article_id), db)
        clusters_transformed.append(article_id_to_article)
    return clusters_transformed
