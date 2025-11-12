#%%
import json
from openai import OpenAI

# Configura il client con l'API key e l'URL di base
# questa è la parte che va modificata per usare altri provider, ad esempio OpenAI, Groq, Gemini etc.
base_url = "http://130.251.104.214:11434/v1/"   # URL del nostro server Ollama! (si accede con vpn da remoto!)
client = OpenAI(api_key="-", base_url=base_url)


# %%
# ottieni la lista dei modelli disponibili sul nostro server
models = client.models.list()
print("Modelli disponibili:")
for m in models.data:
    print(f"- {m.id}")


#%%
# Effettua la chiamata API
# Crea una chat completion con un prompt specifico
model = "gemma3:4b"  # Scegli il modello tra quelli disponibili

print(f"\nEsempio di chiamata API per creare una chat completion usando il modello {model}:\n")

response = client.chat.completions.create(
    model=model,
    messages=[
    {"role": "system", "content": "Sei un assistente che parla solo in rima e risponde brevemente."}, # system prompt che condiziona il comportamento del modello
    {"role": "user", "content": "Ciao, come stai?"}                             # user prompt con la domanda dell'utente
])

print("Risposta completa ottenuta dalla chiamata API:")
# Estrai e stampa il contenuto della prima (ed unica) risposta
print(response.model_dump_json(indent=2))



# %%
