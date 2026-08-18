import os
import requests
from app.db import query
from app.ai import vector_store
import app.db.query

def run_add_articles_and_clusters_job() -> dict[str, object]:
    base_url = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")

    steps = [
        ("articles_ingest", "/articles/ingest"),
        ("embed_articles", "/embed/embed"),
        ("process_info_clusters", "/infos/process_info_clusters"),
    ]

    results: dict[str, object] = {}
    for step_name, path in steps:
        response = requests.post(f"{base_url}{path}", timeout=900, headers={"Content-Type": "application/json", "User-Agent": "Google-Cloud-Scheduler"})
        response.raise_for_status()
        results[step_name] = response.json()

    return results


def run_delete_6_days_old_call_job(db):
    articles_ids_to_delete = query.get_articles_ids_older_than_6_days(db)
    if not articles_ids_to_delete:
        return 0
    vector_store.delete_embeddings_by_ids([str(art_id) for art_id in articles_ids_to_delete])
    query.delete_info_clusters_articles_with_ids(articles_ids_to_delete, db)
    db.commit()

    query.delete_articles_with_ids(articles_ids_to_delete, db)
    db.commit()

    info_clusters_size_1 = query.get_info_clusters_size_1(db)
    info_clusters_size_1_ids = [cluster.id for cluster in info_clusters_size_1]
    query.delete_info_clusters_articles_with_clusters_ids(info_clusters_size_1_ids, db)
    db.commit()

    query.delete_info_clusters_without_articles(db)
    db.commit()
    db.close()
    return len(articles_ids_to_delete)