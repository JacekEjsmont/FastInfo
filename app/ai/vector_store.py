import os
from app.ai.embeddings import embed_text
from app.db import query
from pinecone import Pinecone

PINECONE_NAME = "Pinecone"
USED_VECTOR_DB = PINECONE_NAME
INDEX_NAME = "fast-info-openai-index"

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=PINECONE_API_KEY)
fast_info_index = pc.Index(INDEX_NAME)

def get_all_embeddings():
    if USED_VECTOR_DB == PINECONE_NAME:
        return get_all_pinecone_embeddings()
    return None


def get_all_pinecone_embeddings():
    all_ids = get_all_embedding_ids()
    all_ids_each_1000 = [all_ids[i:i + 1000] for i in range(0, len(all_ids), 1000)]
    vectors = {}
    for ids in all_ids_each_1000:
        fetch_record = fast_info_index.fetch(ids=ids)
        vectors.update(fetch_record.vectors)
    all_vectors = {rec.id: rec.values for rec in vectors.values()}
    return dict(sorted(all_vectors.items()))

def get_all_embedding_ids():
    if USED_VECTOR_DB == PINECONE_NAME:
        return get_all_embedding_ids_pinecone()
    return None

def get_all_embedding_ids_pinecone():
    all_ids = []
    for list_record in fast_info_index.list():
        for vector in list_record.vectors:
            all_ids.append(vector["id"])
    return all_ids

def store_embeddings():
    if USED_VECTOR_DB == PINECONE_NAME:
        store_embeddings_pinecone()

def store_embeddings_pinecone():
    articles = query.get_articles_not_embedded_yet()
    vectors = []
    for article in articles:
        summary_text = f"{article.summary_pl}"
        embedding_summary = embed_text(summary_text)
        if not embedding_summary:
            continue
        vector = {"id": str(article.id),
                  "values": embedding_summary,
                  "metadata": {"title": article.title, "source": article.source, "topic": article.topic}
                  }
        vectors.append(vector)
    fast_info_index.upsert(vectors=vectors)