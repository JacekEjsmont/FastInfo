from fastapi import APIRouter
from app.ai import vector_store

router = APIRouter(prefix="/embed")

@router.get("/all_embeddings")
def all_embeddings():
    articles_embeddings = vector_store.get_all_embeddings()
    # return articles_embeddings.get("embeddings").tolist()
    return articles_embeddings.get("ids")

@router.get("/all_embeddings_by_tags")
def all_embeddings():
    articles_embeddings = vector_store.get_all_embeddings_by_tags()
    # return articles_embeddings.get("embeddings").tolist()
    return articles_embeddings.get("ids")

@router.post("/embed")
def embed():
    vector_store.store_embeddings()
    return {"status": "embedded"}
