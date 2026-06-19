from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# model "all-MiniLM-L6-v2" dobry lekki ale tylko po angielsku.
# model "paraphrase-multilingual-MiniLM-L12-v2" troche gorszy ale, radzi sobie po polsku i angielsku
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", token=HF_TOKEN)
modelMultiLang = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", token=HF_TOKEN)

def embed_text(text: str):
    return model.encode(text).tolist()

def embed_tags(tags: list):
    return modelMultiLang.encode(tags).tolist()
