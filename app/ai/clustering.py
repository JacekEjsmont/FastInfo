
from scipy.spatial import distance

def cluster_by_similarity(embeddings, ids, threshold=0.35):
    """ Groups embeddings of articles by their similarity scores
    :param threshold: bigger value means less similar articles. Lower more similar
    :param embeddings: article embeddings
    :param ids: article ids
    :return: list of list of tuples containing grouped articles ids with their embeddings (article_id, embedding)"""
    clusters = []

    for index, emb in enumerate(embeddings):
        article_id = ids[index]
        added = False

        for cluster in clusters:

            dist = distance.cosine(emb, cluster[0][1])

            if dist < threshold:
                cluster.append((article_id, emb))
                added = True
                break

        if not added:
            clusters.append([(article_id, emb)])

    return clusters
