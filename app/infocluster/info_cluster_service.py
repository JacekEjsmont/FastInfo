from app.ai.vector_store import get_all_embeddings
from app.ai.clustering import cluster_by_similarity
from app.ai.info_cluster_analysis_service import cluster_ai_analysis
from app.db.database import SessionLocal
from app.db.models import InfoCluster, Article
from app.db import query
import datetime
import json

def break_if_topic_is_weather(topic):
    if "Pogoda" in topic or "Meteorologia" in topic or "Środowisko i Klimat" in topic:
        return True
    return False

def delete_duplicates(articles_ids_per_cluster):
    def find_duplicates(items):
        seen = set()
        duplicates = []

        for item in items:
            key = tuple(item)

            if key in seen:
                if list(item) not in duplicates:
                    duplicates.append(list(item))
            else:
                seen.add(key)

        return duplicates
    duplicates = find_duplicates(articles_ids_per_cluster)
    for duplicate in duplicates:
        articles_ids_per_cluster.remove(duplicate)


def detect_clusters(db):
    embeddings_data = get_all_embeddings()
    articles_ids_per_cluster = query.get_articles_ids_per_cluster(db)
    delete_duplicates(articles_ids_per_cluster)
    current_clusters = [[(str(article_id), embeddings_data.get(str(article_id))) for article_id in articles_cluster] for articles_cluster in articles_ids_per_cluster]
    if not current_clusters:
        current_clusters = []
    info_clusters_first_run = cluster_by_similarity(embeddings_data, clusters=current_clusters)
    info_clusters = cluster_by_similarity(embeddings_data, clusters=info_clusters_first_run)
    return info_clusters

def nothing_changed_in_info_cluster(info_cluster, cluster):
    if not info_cluster:
        return False #new event/cluster
    if len(info_cluster.articles) != len(cluster):
        return False #new articles in the event/cluster
    return True

def create_new_info_cluster(info_cluster_id):
    info_cluster = InfoCluster(title="Title placeholder", id=info_cluster_id)
    return info_cluster

def update_info_cluster(info_cluster, cluster, db):
    articles_in_info_cluster = []
    for article_emb_record in cluster:
        article_id = article_emb_record[0]
        article = query.get_article_by_id(article_id, db)
        if break_if_topic_is_weather(article.topic):
            break
        articles_in_info_cluster.append(article.__dict__)
        article_ids_already_in_cluster = [article.id for article  in info_cluster.articles]
        if article_id not in article_ids_already_in_cluster:
            info_cluster.articles.append(article)
    if len(articles_in_info_cluster) == 0:
        return False
    info_cluster_data_raw_string = cluster_ai_analysis(articles_in_info_cluster)
    info_cluster_data = json.loads(info_cluster_data_raw_string)
    info_cluster.title = info_cluster_data.get("title")
    info_cluster.summary = info_cluster_data.get("summary_pl")
    info_cluster.updated_at = datetime.datetime.utcnow()
    return True


def refresh_info_clusters():
    """first function in flow of creating info clusters"""
    db = SessionLocal()
    clusters = detect_clusters(db)
    print("ai articles clustering processing...")
    for cluster in clusters:
        if len(cluster) <= 1:
            continue
        if cluster[0][0] == cluster[1][0]:
            continue
        info_cluster_id = cluster[0][0] + cluster[1][0]
        info_cluster = db.query(InfoCluster).get(info_cluster_id)
        if nothing_changed_in_info_cluster(info_cluster, cluster):
            continue
        ids_already_in_some_cluster = query.get_str_articles_ids_already_in_cluster(db)
        if not info_cluster and cluster[0][0] not in ids_already_in_some_cluster and cluster[1][0] not in ids_already_in_some_cluster:
            info_cluster = create_new_info_cluster(info_cluster_id)
        else:
            continue
        cluster_updated = update_info_cluster(info_cluster, cluster, db)
        print(info_cluster.title)
        print("cluster_updated", cluster_updated)
        if cluster_updated:
            db.merge(info_cluster)
            db.commit()
    db.close()