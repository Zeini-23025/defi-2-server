import openai

openai.api_key = ""  # Remplace par ta clé API

def generate_word_variants(word):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Conjuguer le mot '{word}' en hassaniya",
        max_tokens=50,
        n=3,
        temperature=0.7
    )
    
    generated_variants = [choice.text.strip() for choice in response.choices]
    return generated_variants

# Exemple d'utilisation
word_variants = generate_word_variants("kteb")
for variant in word_variants:
    print(variant)
