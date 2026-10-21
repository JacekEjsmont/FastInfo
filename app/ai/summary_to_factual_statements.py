import ollama
from app.ai import few_shot_classification_data

context = f"""Zamień streszczenie podane w "Streszczenie" na pojedyncze twierdzenia faktograficzne. Używaj tylko informacji ze "Streszczenie"
Zwróć listę [] ze stworzonymi pojedyńczymi twierdzeniami faktograficznymi."""


def transform_summary_to_factual_statements(text):
    prompt_messages = [
    {"role": "system", "content": context},
    {"role": "user", "content":"Streszczenie: " + few_shot_classification_data.factual_statements_input},
    {"role": "assistant", "content": few_shot_classification_data.factual_statements_output},
    {"role": "user", "content": "Streszczenie: " + text},
    ]
    resp = ollama.chat(
        model="bielik-11",
        messages=prompt_messages,
        options={"num_ctx": 8192, "temperature": 0.2},
    )
    resp_cont = resp.message.content
    # print(resp_cont)
    return resp_cont
