
from scipy.spatial import distance

def cluster_by_similarity(embeddings_data, threshold=0.30, clusters=[]):
    """ Groups embeddings of articles by their similarity scores
    :param clusters: cluster to start with. Default is empty
    :param threshold: bigger value means less similar articles. Lower more similar
    :param embeddings_data: map {article_id, embeddings}
    :return: list of list of tuples containing grouped articles ids with their embeddings (article_id, embedding)"""

    for article_id in embeddings_data:
        emb = embeddings_data[article_id]
        added = False
        for cluster in clusters:
            already_added_ids = [element[0] for element in cluster]
            if article_id in already_added_ids:
                added = True
                break
            list_of_distances = []
            for already_added in cluster:
                d = distance.cosine(emb, already_added[1])
                if article_id is not already_added[0]:
                    list_of_distances.append(d)

            for dist in list_of_distances:
                if dist < threshold:
                    cluster.append((article_id, emb))
                    added = True
                    break
            if added:
                break

        if not added:
            clusters.append([(article_id, emb)])

    return clusters
