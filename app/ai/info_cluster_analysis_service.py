import json
from operator import itemgetter
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
open_ai_key = os.getenv("OPEN_AI_KEY")
client = OpenAI(api_key=open_ai_key)

context = """Dostaniesz json string o strukturze: {claims:[]} Pole 'claims będzie zawierać liste z kluczowymi informacjami z artykułów gazet.
Zwróć JSON z polami:
summary_pl: Na podstawie informacji w polu 'claims' stwórz opis czego dotyczą informacje. Maks 2-4 zdania.
title: tytuł dla stworzonego opisu.

Dodatkowe reguły:
- Używaj tylko informacji zawartych w polu 'claims'
- nie spekuluj
- zwróć tylko i wyłącznie poprawny JSON"""

def cluster_ai_analysis(articles_in_info_cluster):
    claims = []
    for article in articles_in_info_cluster:
        claims.append(json.loads(article.get("claims")))
    claims_json = {"claims" : claims}

    prompt_messages = [
        {"role": "developer", "content": context},
        {"role": "user", "content": f"""Json z danymi: {json.dumps(claims_json)}"""},
    ]
    response = client.responses.create(
        model="gpt-5-nano",
        timeout=180,
        reasoning={"effort": "low"},
        input=prompt_messages
    )
    return response.output_text