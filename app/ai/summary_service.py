from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
open_ai_key = os.getenv("OPEN_AI_KEY")
client = OpenAI(api_key=open_ai_key)

LIST_OF_TOPICS = ["Nauka i Technologie", "Społeczeństwo", "Geopolityka i Konflikty zbrojne", "Ze Świata", "Polityka i Prawo Polski", "Gospodarka i Biznes", "Wewnątrz Polski", "Sport", "Środowisko i Klimat", "Kultura i Rozrywka"]

context = f"""Jesteś profesjonalnym redaktorem wiadomości, Wyciągnij z artykułu dane i stwórz strukture.
Zwróć JSON z polami:
summary_pl: zwięzłe streszczenie artykułu, zachowaj kluczowe fakty i kontekst i skup się na najważniejszych informacjach, maksymalnie 4–5 zdań.
title: tytuł dla stworzonego streszczenia.
topic: kategoria artykułu. Dopasuj kategorie z tej listy: {str(LIST_OF_TOPICS)}. Lub jeśli nic z podanych nie pasuje wpisz "Inne"
claims: zgłoszone faktyczne stwierdzenia.

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
