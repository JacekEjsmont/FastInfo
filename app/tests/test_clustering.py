import pytest
from app.ai.clustering import cluster_by_similarity
import data_for_testing


def test_cluster_for_similar_subjects():
    embeddings_data = data_for_testing.embeddings_data_1
    result = cluster_by_similarity(embeddings_data)
    article_ids_groups = [[article_emb_data[0] for article_emb_data in cluster] for cluster in result]
    assert article_ids_groups.sort() == data_for_testing.correct_groups_for_embeddings_data_1.sort()
