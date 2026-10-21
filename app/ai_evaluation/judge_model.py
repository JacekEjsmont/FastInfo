from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
open_ai_key = os.getenv("OPEN_AI_KEY")
client = OpenAI(api_key=open_ai_key)

context = """Otrzymasz "Zdania" w formie listy [] i otrzymasz "Artykuł". 
Oceń każde zdanie z listy "Zdania", ustalając czy jest prawdą według informacji w Arykuł.
Zwróć json z listą map: 
[
{zdanie: zdanie z listy,
 potwierdzone: Możliwe wartości to tak/nie. "tak" jeśli zdanie można uznać prawdziwe w kontekście Artykuł. "nie" gdy nie jest potwierdzone.
 uzasadnienie: uzasadnienie dlaczego zdanie jest potwierdzone jako tak lub nie,
 }
 ]
Zwróć tylko i wyłącznie poprawny json. Używaj tylko i wyłącznie przekazanych informacji.  
"""

def judge_article_faithfulness(article_text, claims):
    prompt_messages = [
        {"role": "developer", "content": context},
        {"role": "user", "content": f"""Artykuł: {article_text} \n Zdania: {str(claims)}"""},
    ]
    response = client.responses.create(
        model="gpt-5.6-luna",
        timeout=180,
        input=prompt_messages)
    return response.output_text



context_for_one_statement = """ Sprawdź czy co jest stwierdzone w "Zdanie" jest prawdziwe na podstawie informacji w "Tekst". Sprawdzaj dokładnie i bądź krytyczny.
Otrzymasz :
Tekst: lista z tekstem na podstawie którego będziesz stwierdzał czy coś jest prawdą czy nie
Zdanie: zdanie które trzeba sprawdzić
Odpowiedz tylko i wyłącznie w takim formacie JSON: "{"potwierdzone": "tak" jeśli Zdanie da się potwierdzić w Tekst lub "nie" jeśli nie da się potwierdzić lub nie wiem jeśli ciężko stwierdzić
         "fragment": fragment z Tekst na podstawie którego Zdanie zostało potwierdzone. Lub puste jeśli się nie da potwierdzić}"

"""


def judge_article_faithfulness_for_one_statement(best_matching_text_chunks, statement):
    prompt_messages = [
        {"role": "developer", "content": context_for_one_statement},
        {"role": "user", "content": f"""Tekst: {str(best_matching_text_chunks)} \n Zdanie: {str(statement)}"""},
    ]
    response = client.responses.create(
        model="gpt-5.6-luna",
        timeout=180,
        input=prompt_messages)
    return response.output_text

