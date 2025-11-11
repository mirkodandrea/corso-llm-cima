#%%
from openai import OpenAI

# Configura il client con l'API key e l'URL di base
# questa è la parte che va modificata per usare altri provider, ad esempio OpenAI, Groq, Gemini etc.
base_url = "http://130.251.104.214:11434/v1/"   # URL del nostro server Ollama! (si accede con vpn da remoto!)
client = OpenAI(api_key="-", base_url=base_url)
model = "gpt-oss:20b"

#%%
# Effettua la chiamata API
# Crea una chat completion con un prompt specifico
response = client.chat.completions.create(
    model=model, # Scegli il modello
    messages=[
    {"role": "system", "content": "Sei un assistente che parla solo in rima."},
    {"role": "user", "content": "Ciao, come stai?"}
])

# Estrai e stampa il contenuto della prima (ed unica) risposta
print(response.choices[0].message.content)

# %%
# Stampa l'intera risposta JSON per ispezione
import json
print(json.dumps(response.model_dump(), indent=2))


#%% esempio di uso dei parametri

# Effettua la chiamata API con parametri personalizzati
response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "user", "content": "Raccontami una barzelletta sugli elefanti."}
    ],
    temperature=0.7,  # Controlla la creatività della risposta
    max_tokens=150    # Limita la lunghezza della risposta
)
print(response.choices[0].message.content)

# %%
