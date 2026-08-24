import datetime

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

def delete_all_articles():
    stmt = delete(Article).where(Article.id.isnot(None))
    db = SessionLocal()
    db.execute(stmt)
    db.commit()
    db.close()

def delete_articles_with_ids(article_ids, db: Session):
    query = db.query(Article).filter(Article.id.in_(article_ids))
    query.delete(synchronize_session=False)
    db.commit()

def delete_info_clusters_articles_with_ids(article_ids, db: Session):
    if not article_ids:
        return

    stmt = delete(info_clusters_articles).where(info_clusters_articles.c.article_id.in_(article_ids))
    db.execute(stmt)
    db.commit()

def delete_info_clusters_articles_with_clusters_ids(clusters_ids, db: Session):
    if not clusters_ids:
        return

    stmt = delete(info_clusters_articles).where(info_clusters_articles.c.infocluster_id.in_(clusters_ids))
    db.execute(stmt)
    db.commit()

def delete_info_clusters_without_articles(db: Session):
    stmt = delete(InfoCluster).where(~InfoCluster.articles.any())
    db.execute(stmt)
    db.commit()

def delete_where_claims_empty():
    stmt = delete(Article).where(Article.claims.is_(None))
    db = SessionLocal()
    db.execute(stmt)
    db.commit()
    db.close()

def get_all_info_clusters(db: Session):
    all_info_clusters = db.query(InfoCluster).filter(InfoCluster.id.isnot(None)).all()
    return all_info_clusters

def get_articles_ids_per_cluster(db: Session):
    all_info_clusters = db.query(InfoCluster).filter(InfoCluster.id.isnot(None)).all()
    articles_in_info_clusters = [[article.id for article in cluster.articles] for cluster in all_info_clusters]
    for article_ids_list in articles_in_info_clusters:
        article_ids_list.sort()
    return articles_in_info_clusters

def get_str_articles_ids_already_in_cluster(db: Session):
    all_info_clusters = db.query(InfoCluster).filter(InfoCluster.id.isnot(None)).all()
    articles_ids = []
    for cluster in all_info_clusters:
        for article in cluster.articles:
            articles_ids.append(str(article.id))
    return articles_ids

def get_info_clusters_recent(db: Session):
    return (
        db.query(InfoCluster)
        .filter(InfoCluster.id.isnot(None))
        .order_by(desc(InfoCluster.updated_at))
        .all()
    )

def get_info_clusters_size_1(db: Session):
    return (
        db.query(InfoCluster)
        .join(info_clusters_articles, InfoCluster.id == info_clusters_articles.c.infocluster_id)
        .group_by(InfoCluster.id)
        .having(func.count(func.distinct(info_clusters_articles.c.article_id)) == 1)
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

def get_articles_ids_older_than(db: Session, days: int):
    cutoff_date = datetime.datetime.utcnow() - datetime.timedelta(days=days)
    return db.scalars(
        select(Article.id)
        .where(Article.published_at < cutoff_date)
        .order_by(desc(Article.published_at))
    ).all()

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
