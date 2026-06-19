from transformers import AutoTokenizer, MarianMTModel


def split_without_breaking_words(text, max_length=15):
    words = text.split()
    chunks = []
    current_chunk = ""

    for word in words:
        # sprawdzamy czy dodanie słowa przekroczy limit
        if len(current_chunk) + len(word) + (1 if current_chunk else 0) <= max_length:
            if current_chunk:
                current_chunk += " "
            current_chunk += word
        else:
            chunks.append(current_chunk)
            current_chunk = word
    if current_chunk:
        chunks.append(current_chunk)

    return chunks

model_name_translate = "allegro/BiDi-eng-pol"
tokenizer = AutoTokenizer.from_pretrained(model_name_translate)
model_translation = MarianMTModel.from_pretrained(model_name_translate)
def translate_text(text: str):
    """Detects language and translate automatically between Polish and English"""
    batch_to_translate = split_without_breaking_words(text, 300) #Model ma problem powyżej 300
    translations = model_translation.generate(**tokenizer(batch_to_translate, return_tensors="pt", padding=True))
    decoded_translation = tokenizer.batch_decode(translations, skip_special_tokens=True, clean_up_tokenization_spaces=True)
    translated_text = " ".join(decoded_translation)
    return translated_text
