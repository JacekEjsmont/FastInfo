import os

import requests


def run_add_articles_and_clusters_job() -> dict[str, object]:
    base_url = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")

    steps = [
        ("articles_ingest", "/articles/ingest"),
        ("embed_articles", "/embed/embed"),
        ("process_info_clusters", "/infos/process_info_clusters"),
    ]

    results: dict[str, object] = {}
    for step_name, path in steps:
        response = requests.post(f"{base_url}{path}", timeout=900)
        response.raise_for_status()
        results[step_name] = response.json()

    return results


