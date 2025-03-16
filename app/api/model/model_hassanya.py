import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOGETHER_API_KEY = os.getenv("31a2be173d436083abbfcc901f28d537b6116b70b964da5c8c7598a8e5c2225a")

# Fonction pour générer des variantes d'un mot en hassaniya
def generate_words(word):
    # word = request.GET.get("word", "shrab")
    url = "https://api.together.xyz/v1/completions"
    
    headers = {
        "Authorization": f"Bearer {'31a2be173d436083abbfcc901f28d537b6116b70b964da5c8c7598a8e5c2225a'}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "prompt": f"Génère des formes dérivées et conjuguées du mot '{word}' en hassaniya. sans explication svp just les formes s'ils existent (7 mots au max svp) en arabe",
        "max_tokens": 100
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    return result


