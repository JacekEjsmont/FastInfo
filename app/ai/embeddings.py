
from openai import OpenAI
from dotenv import load_dotenv
import os
from sentence_transformers import SentenceTransformer


load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", token=HF_TOKEN)
modelMultiLang = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", token=HF_TOKEN)

def embed_text_transformers(text: str):
    return model.encode(text).tolist()

def embed_tags_transformers(tags: list):
    return modelMultiLang.encode(tags).tolist()


open_ai_key = os.getenv("OPEN_AI_KEY")
client = OpenAI(api_key=open_ai_key)

def embed_text(text: str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    response_dict = response.model_dump()
    return response_dict["data"][0]["embedding"]

def embed_tags(tags: list):
    pass