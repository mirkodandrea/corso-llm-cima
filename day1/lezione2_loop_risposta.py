#%%
from openai import OpenAI
import json

# Configura il client con l'API key e l'URL di base
# questa è la parte che va modificata per usare altri provider, ad esempio OpenAI, Groq, Gemini etc.
base_url = "http://130.251.104.214:11434/v1/"   # URL del nostro server Ollama! (si accede con vpn da remoto!)
client = OpenAI(api_key="-", base_url=base_url)
model = "gemma3:4b"  # Scegli il modello tra quelli disponibili

print("Inizio della chat con il modello LLM. Digita 'exit' o 'quit' per terminare.")

# dimostrazione di un loop per più richieste con input utente
# inizializza la lista dei messaggi con il messaggio di sistema
messages = [
    {"role": "system", "content": "Sei un utile assistente che risponde brevemente."},
]

while True:
    # Ottieni l'input dell'utente
    user_input = input("Utente: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Uscita dalla chat.")
        break    
    # Aggiungi il messaggio dell'utente alla lista dei messaggi
    message = {"role": "user", "content": user_input}
    messages.append(message)

    # Effettua la chiamata API per ottenere la risposta del modello
    response = client.chat.completions.create(
        model=model,
        messages=messages,                                      # type:ignore
    )   
    response = response.choices[0].message.content              # type:ignore
    print(f"Assistente: {response}")

    # Aggiungi la risposta del modello alla lista dei messaggi
    messages.append({"role": "assistant", "content": response}) # type:ignore

# Stampa l'intera conversazione in formato JSON
print("Conversazione in formato JSON:")
print(json.dumps(messages, indent=2))