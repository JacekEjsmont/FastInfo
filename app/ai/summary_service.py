# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# model_name_summary = "sshleifer/distilbart-cnn-12-6"
# tokenizer = AutoTokenizer.from_pretrained(model_name_summary)
# model = AutoModelForSeq2SeqLM.from_pretrained(model_name_summary)
#
#
# def split_without_breaking_words(text, max_length=15):
#     words = text.split()
#     chunks = []
#     current_chunk = ""
#
#     for word in words:
#         # sprawdzamy czy dodanie słowa przekroczy limit
#         if len(current_chunk) + len(word) + (1 if current_chunk else 0) <= max_length:
#             if current_chunk:
#                 current_chunk += " "
#             current_chunk += word
#         else:
#             chunks.append(current_chunk)
#             current_chunk = word
#     if current_chunk:
#         chunks.append(current_chunk)
#
#     return chunks
#
#
#
# def create_article_summary(text):
#     batch_of_text = split_without_breaking_words(text, 500)
#     inputs = tokenizer(batch_of_text, return_tensors="pt", padding=True)
#     summary_ids = model.generate(inputs["input_ids"], num_beams=2, min_length=0, max_length=150)
#     result = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)
#     return " ".join(result)
#------------------------------------------------------------------------------------------------------------------------------

# tokenizer = AutoTokenizer.from_pretrained( "meta-llama/Meta-Llama-3.1-8B-Instruct", token=HF_TOKEN )


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
        # {"role": "developer", "content": base_context + tier1_context + tier2_context + tier3_context + final_context},
        # {"role": "developer", "content": context},
        # {"role": "user", "content": f"""Zrób streszeczenie artykułu: {text}"""},
        {"role": "developer", "content": context},
        {"role": "user", "content": f"""Artykuł: {text}"""},
    ]
    response = client.responses.create(
        model="gpt-5.4-nano",
        timeout=180,
        input=prompt_messages
    )
    return response.output_text


# TO RACZEJ DO OMINIECIA
# Analyze the narrative framing of this news article.
#
# Return JSON with:
#
# main_actor: who is presented as the main actor
# action: what action is described
# framing: how the event is framed (e.g. attack, response, escalation)
# tone: tone of the article (neutral, critical, supportive)
#
# Rules:
# - keep answers short
# - use only information present in the text
# - output valid JSON
#
# Article summary:
# {SUMMARY}


# You are analyzing multiple news sources reporting the same event.
#
# Extract:
# event_title
# event_summary
# event_image
# confirmed_facts:
# facts reported by multiple sources
#
# disputed_claims:
# claims that differ or contradict
#
# unique_claims:
# claims reported by only one source
#
# additional_context:
# what is story behind, what is orign of this event
#
# Return JSON.
#
# Articles claims:
# {CLAIMS}