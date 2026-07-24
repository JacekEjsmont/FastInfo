from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
open_ai_key = os.getenv("OPEN_AI_KEY")
client = OpenAI(api_key=open_ai_key)

MAP_OF_TOPIC = {"Nauka i Technologie" : "Wszystko co związane Nauką, Technologią, Wynalazkami, AI w Polsce i na świecie",
                "Społeczeństwo" : "Tematy dotyczące społeczeństwa i życia w polsce i na świecie",
                "Polityka i Prawo Polski" : "Tematy dotyczące Polityki wewnątrz Polski i Prawa w Polsce",
                "Gospodarka i Biznes" : "Tematy dotyczące Gospodarki biznesu i finansów",
                "Geopolityka i Konflikty zbrojne" : "Wydarzenia Geopolityczne i Konflikty zbrojne",
                "Ze Świata" : "Wydarzenia polityczne i nie polityczne tylko po za Polską nie pasujące do kategorii Geopolityka i Konflikty zbrojne jak i Gospodarka i Biznes, Nauka",
                "Wydarzenia z Polski" : "Wydarzenia z Polski nietożsame z polityką, gospodarką, biznezem, prawem, finansami, nauką",
                "Sport" : "Wydarzenia sportowe z Polski i ze Świata",
                "Kataklizmy" : "Kataklizmy w polsce i na świecie",
                "Środowisko i Klimat" : "Wydarzenia związane z klimatem i środowiskiem, pogodą w polsce i na świecie",
                "Kultura i Rozrywka" : "Kwestie związane z kulturą i rozrywką w polsce i na świecie",
                }
LIST_OF_TOPICS = ["Nauka i Technologie", "Społeczeństwo", "Geopolityka i Konflikty zbrojne", "Ze Świata", "Polityka i Prawo Polski", "Gospodarka i Biznes", "Wydarzenia z Polski", "Sport", "Środowisko i Klimat", "Kultura i Rozrywka", "Kataklizmy"]

context = f"""Jesteś profesjonalnym redaktorem wiadomości, Wyciągnij z artykułu dane i stwórz strukture.
Zwróć JSON z polami:
summary_pl: zwięzłe streszczenie artykułu, zachowaj kluczowe fakty i kontekst i skup się na najważniejszych informacjach, maksymalnie 4–5 zdań.
title: tytuł dla stworzonego streszczenia.
topic: kategoria artykułu. Dopasuj kategorie na podstawie tej mapy: {str(MAP_OF_TOPIC)}. Gdzie klucz mapy to kategoria a wartość mapy to wytyczne do przydzielania kategori.
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
