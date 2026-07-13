import os
import chromadb
from app.ai.embeddings import embed_text, embed_tags
from app.db import query
from pinecone import Pinecone

PINECONE_NAME = "Pinecone"
CHROMA_NAME = "Chroma"
USED_VECTOR_DB = PINECONE_NAME

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=PINECONE_API_KEY)
fast_info_index = pc.Index("fast-info-index")

client = chromadb.PersistentClient(path="/chromaDatabase")
collection_by_summary = client.get_or_create_collection(name="articles_summary")
collection_by_tags = client.get_or_create_collection(name="articles_tags")
old_collection = client.get_or_create_collection(name="articles")

def delete_all_collections():
    client.delete_collection(name="articles")
    client.delete_collection(name="articles_summary")
    client.delete_collection(name="articles_tags")

def add_embedding_by_summary(article_id: int, embedding, metadata: dict):
    collection_by_summary.add(
        ids=[str(article_id)],
        embeddings=[embedding],
        metadatas=[metadata]
    )

def delete_embedding_by_ids(article_ids: list):
    """:param article_ids where ids must be strings"""
    collection_by_summary.delete(ids=article_ids)

def add_embedding_by_tags(article_id: int, embedding, metadata: dict):
    collection_by_tags.add(
        ids=[str(article_id)],
        embeddings=[embedding],
        metadatas=[metadata]
    )

def get_all_embeddings():
    if USED_VECTOR_DB == PINECONE_NAME:
        return get_all_pinecone_embeddings()
    elif USED_VECTOR_DB == CHROMA_NAME:
        return get_all_chroma_embeddings()
    return None

def get_all_chroma_embeddings():
    return collection_by_summary.get(include=["embeddings", "metadatas"])

def get_all_pinecone_embeddings():
    all_ids = get_all_embedding_ids()
    all_ids_each_1000 = [all_ids[i:i + 1000] for i in range(0, len(all_ids), 1000)]
    vectors = {}
    for ids in all_ids_each_1000:
        fetch_record = fast_info_index.fetch(ids=ids)
        vectors.update(fetch_record.vectors)
    all_vectors = {rec.id: rec.values for rec in vectors.values()}
    return dict(sorted(all_vectors.items()))

def get_all_embeddings_by_tags():
    return collection_by_tags.get(include=["embeddings", "metadatas"])

def get_all_embedding_ids():
    if USED_VECTOR_DB == PINECONE_NAME:
        return get_all_embedding_ids_pinecone()
    elif USED_VECTOR_DB == CHROMA_NAME:
        return get_all_embeddings_chroma()
    return None

def get_all_embeddings_chroma():
    return collection_by_summary.get().get("ids")

def get_all_embedding_ids_pinecone():
    all_ids = []
    for list_record in fast_info_index.list():
        for vector in list_record.vectors:
            all_ids.append(vector["id"])
    return all_ids

def store_embeddings():
    if USED_VECTOR_DB == PINECONE_NAME:
        store_embeddings_pinecone()
    elif USED_VECTOR_DB == CHROMA_NAME:
        store_embeddings_chroma()

def store_embeddings_chroma():
    articles = query.get_articles_not_embedded_yet()
    for article in articles:
        summary_text = f"{article.summary_eng}"
        embedding_summary = embed_text(summary_text)
        add_embedding_by_summary(
            article.id,
            embedding_summary,
            {
                "title": article.title,
                "source": article.source,
                "topic": article.topic
            }
        )

def store_embeddings_pinecone():
    articles = query.get_articles_not_embedded_yet()
    vectors = []
    for article in articles:
        summary_text = f"{article.summary_eng}"
        embedding_summary = embed_text(summary_text)
        if not embedding_summary:
            continue
        vector = {"id": str(article.id),
                  "values": embedding_summary,
                  "metadata": {"title": article.title, "source": article.source, "topic": article.topic}
                  }
        vectors.append(vector)
    fast_info_index.upsert(vectors=vectors)