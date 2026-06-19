import chromadb
from app.ai.embeddings import embed_text, embed_tags
from app.db import query

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
    return collection_by_summary.get(include=["embeddings", "metadatas"])

def get_all_embeddings_by_tags():
    return collection_by_tags.get(include=["embeddings", "metadatas"])

def get_all_embedding_ids():
    return collection_by_summary.get().get("ids")

def store_embeddings():
    articles = query.get_articles_not_embedded_yet()
    for article in articles:
        summary_text = f"{article.summary_eng}"
        embedding_summary = embed_text(summary_text)
        add_embedding_by_summary(
            article.id,
            embedding_summary,
            {
                "title": article.title,
                "source": article.source
            }
        )
        if not article.actors and not article.locations and not article.topic:
            continue
        embedding_tags = embed_tags(article.actors + article.locations + article.topic)
        add_embedding_by_tags(
            article.id,
            embedding_tags,
            {
                "title": article.title,
                "source": article.source
            }
        )
