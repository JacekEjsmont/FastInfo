from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
open_ai_key = os.getenv("OPEN_AI_KEY")
client = OpenAI(api_key=open_ai_key)

context = """Jesteś profesjonalnym redaktorem wiadomości, Wyciągnij z artykułu dane i stwórz strukture.
Zwróć JSON z polami:
summary_pl: zwięzłe streszczenie artykułu, zachowaj kluczowe fakty i kontekst i skup się na najważniejszych informacjach, maksymalnie 4–5 zdań.
title: tytuł dla stworzonego streszczenia.
actors: ludzie, organizacje, kraje.
locations: miasta, kraje, regiony.
topic: rodzaj tematu artykułu np: "Technologie" lub "Geopolityka" lub "Finanse" lub "Prawo" lub "Konflikty zbrojne" itd.
claims: zgłoszone faktyczne stwierdzenia.
uncertainties: kwestionowane lub niejasne informacje.

Dodatkowe reguły:
- Używaj tylko informacji zawartych w artykule
- nie spekuluj
- niech pole "claims" będzie bardzo krótkie 
- unikaj zwrotów "W artykule" "według artykułu" itd
- zwróć tylko i wyłącznie poprawny JSON
- jeśli zauważysz brak treści artykułu, nic nie analizuj i nie streszczaj tylko zwróć pusty JSON"""

def create_article_summary(text):
    prompt_messages = [
        {"role": "developer", "content": context},
        {"role": "user", "content": f"""Artykuł: {text}"""},
    ]
    response = client.responses.create(
        model="gpt-5.4-nano",
        timeout=180,
        input=prompt_messages
    )
    return response.output_text
