import ollama
from app.ai import few_shot_classification_data

context = """Otrzymasz "Zdania" w formie listy [] i otrzymasz "Artykuł". 
Oceń każde zdanie z listy "Zdania", ustalając czy jest prawdą według informacji w Arykuł.
Zwróć json z listą map: 
[
{zdanie: zdanie z listy,
 potwierdzone: Możliwe wartości to tak/nie. "tak" jeśli zdanie można uznać prawdziwe w kontekście Artykuł. "nie" gdy nie da się jednoznacznie stwierdzić że jest prawdziwe.
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
    response = ollama.chat(
        model="bielik-11",
        options={"num_ctx": 8192, "temperature": 0.1},
        messages=prompt_messages    )
    return response.message.content


context_for_one_statement = """Sprawdzasz, czy zdanie zgadza się z tekstem źródłowym. Opierasz się wyłącznie na tym tekście..
Otrzymasz :
Tekst: lista z tekstem źródłowym.
Zdanie: zdanie który trzeba sprawdzić
Odpowiedz tylko i wyłącznie w takim formacie JSON: "{"potwierdzone": "tak" jeśli Zdanie da się zgadza lub "nie" jeśli nie da się nie zgadza lub nie wiem jeśli ciężko stwierdzić
         "fragment": fragment z Tekst na podstawie którego Zdanie zostało potwierdzone. Lub puste jeśli się nie da potwierdzić}"

"""

def judge_article_faithfulness_for_one_statement(best_matching_text_chunks, statement):
    prompt_messages = [
        {"role": "system", "content": context_for_one_statement},
        {"role": "user", "content": f"""{few_shot_classification_data.judge_input}"""},
        {"role": "assistant", "content": f"""{few_shot_classification_data.judge_output}"""},
        {"role": "user", "content": f"""Tekst: {str(best_matching_text_chunks)} \n Zdanie: {str(statement)}"""},
    ]
    response = ollama.chat(
        model="bielik-11",
        options={"num_ctx": 8192, "temperature": 0.1},
        messages=prompt_messages)
    return response.message.content


