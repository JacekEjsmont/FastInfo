import ollama
import json
from app.ai import base_fine_tune_data

context = """Dostaniesz json string o strukturze: {claims:[]} Pole 'claims będzie zawierać liste z informacjami z artykułów gazet.
Zwróć JSON {summary_pl: "", title: ""} gdzie:
summary_pl: Na podstawie informacji w polu 'claims' Bardzo zwięźle opisz czego dotyczą informacje.
title: tytuł dla stworzonego opisu.

Dodatkowe reguły:
- Używaj tylko informacji zawartych w polu 'claims'
- nie spekuluj
- zwróć tylko i wyłącznie poprawny JSON. Tylko 1 { na początku i tylko 1 } na końcu"""



def cluster_ai_analysis(articles_in_info_cluster):
    claims = []
    for article in articles_in_info_cluster:
        # claims.append(json.loads(article.get("claims"))) #Starsza wersja na mniejszej ilości tekstu. Możliwe że będzie trzeba przywrócić
        claims.append(article.get("summary_pl"))
    claims_json = {"claims" : claims}
    print(json.dumps(claims_json))
    prompt_messages = [
        {"role": "developer", "content": context},
        {"role": "user", "content": f"""Json string z danymi: {base_fine_tune_data.cluster_input_2}"""},
        {"role": "assistant", "content": base_fine_tune_data.cluster_output_2},
        {"role": "user", "content": f"""Json string z danymi: {json.dumps(claims_json)}"""},
    ]
    resp = ollama.chat(
        model="bielik-11",
        messages=prompt_messages,
        options={"num_ctx": 8192, "temperature": 0.2},
    )
    resp_cont = resp.message.content
    print(resp_cont)
    return resp_cont