from sqlalchemy import desc, func, select, text
from sqlalchemy.orm import Session
from app.db.models import Article, InfoCluster, info_clusters_articles
from app.db.database import SessionLocal, delete
from app.ai import vector_store

def get_all_articles(db: Session):
    q = db.query(Article)
    all_art = q.filter(Article.id.isnot(None)).all()
    return all_art

def get_article_by_id(article_id: int, db: Session):
    return db.get(Article, article_id)

def get_articles_not_embedded_yet():
    with SessionLocal() as db:
        q = db.query(Article)
        ids_already_embedded = vector_store.get_all_embedding_ids()
        articles = q.filter(~Article.id.in_(ids_already_embedded)).all()
        return articles

def delete_everything():
    stmt = delete(Article).where(Article.id.isnot(None))
    db = SessionLocal()
    db.execute(stmt)
    db.commit()
    db.close()

def delete_where_claims_empty():
    stmt = delete(Article).where(Article.claims.is_(None))
    db = SessionLocal()
    db.execute(stmt)
    db.commit()
    db.close()

def get_all_info_clusters(db: Session):
    return db.query(InfoCluster).filter(InfoCluster.id.isnot(None)).all()

def get_info_clusters_recent(db: Session):
    return (
        db.query(InfoCluster)
        .filter(InfoCluster.id.isnot(None))
        .order_by(desc(InfoCluster.updated_at))
        .all()
    )

def get_info_clusters_recent_with_counts(db: Session):
    thumb_subq = (
        select(Article.img)
        .select_from(Article)
        .join(info_clusters_articles, Article.id == info_clusters_articles.c.article_id)
        .where(info_clusters_articles.c.infocluster_id == InfoCluster.id)
        .where(Article.img.isnot(None))
        .where(Article.img != "")
        .order_by(desc(Article.published_at))
        .limit(1)
        .scalar_subquery()
    )
    return (
        db.query(
            InfoCluster,
            func.count(info_clusters_articles.c.article_id).label("articles_count"),
            thumb_subq.label("thumb_url"),
        )
        .outerjoin(
            info_clusters_articles,
            InfoCluster.id == info_clusters_articles.c.infocluster_id,
        )
        .group_by(InfoCluster.id)
        .order_by(desc(InfoCluster.updated_at))
        .all()
    )

def get_info_cluster_by_id(info_cluster_id: int, db: Session):
    info_cluster = db.get(InfoCluster, info_cluster_id)
    return info_cluster.articles if info_cluster else []

def get_info_cluster_model_by_id(info_cluster_id: int, db: Session):
    return db.get(InfoCluster, info_cluster_id)

def get_articles_for_info_cluster(info_cluster_id: int, db: Session):
    return (
        db.query(Article)
        .join(Article.infoclusters)
        .filter(InfoCluster.id == info_cluster_id)
        .order_by(desc(Article.published_at))
        .all()
    )

def get_articles_without_info_cluster(db: Session):
    return (
        db.query(Article)
        .filter(~Article.infoclusters.any())
        .order_by(desc(Article.published_at))
        .all()
    )

def execute_query(query: str):
    with SessionLocal() as db:
        db.execute(text(query))
        db.commit()

def execute_query_sqlite(query: str):
    pass
    # conn = sqlite3.connect('news.db')
    # c = conn.cursor()
    # c.execute(query)
    # conn.commit()
    # conn.close()