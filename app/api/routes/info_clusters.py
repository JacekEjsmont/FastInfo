from fastapi import APIRouter, Depends
from app.db import query
from sqlalchemy.orm import Session
from app.db.database import get_db

router = APIRouter(prefix="/infos")


@router.get("/all_info_clusters")
def all_info_clusters(db: Session = Depends(get_db)):
    return query.get_all_info_clusters(db)

@router.get("/info_cluster")
def info_cluster(info_cluster_id: str, db: Session = Depends(get_db)):
    return query.get_info_cluster_by_id(info_cluster_id, db)
