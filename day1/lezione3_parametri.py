#%%
from openai import OpenAI

# Configura il client con l'API key e l'URL di base
# questa è la parte che va modificata per usare altri provider, ad esempio OpenAI, Groq, Gemini etc.
base_url = "http://130.251.104.214:11434/v1/"   # URL del nostro server Ollama! (si accede con vpn da remoto!)
client = OpenAI(api_key="-", base_url=base_url)

#%% esempio di uso dei parametri

# Esempio del parametro "temperature" per controllare la creatività della risposta
PROMPT = "Descrivi in 5 parole Savona."
MODEL = "gemma3:4b"

print(f"Esempio di chiamata API con diversi valori del parametro temperature usando il modello {MODEL} e il prompt: {PROMPT}")
for temperature in [0, 1.0, 2.0]:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": PROMPT}],
        temperature=temperature
    )
    print('\n\n------------------------------')
    print(f"Risposta con temperatura {temperature}:")
    print(response.choices[0].message.content)



#%%
# Esempio di utilizzo del parametro max_tokens per limitare la lunghezza della risposta
# Parameter: max_tokens=50
QUERY = "Descrivi in 3 parole cosa fa un computer."
response = client.chat.completions.create(
    model="gemma3:12b",
    messages=[{"role": "user", "content": QUERY}],
    max_tokens=12
)
print('------------------------------')
print(f"{QUERY}")
print("\nRisposta con max_tokens=12:")
print(response.choices[0].message.content)


# attenzione! Le risposte verranno tagliate indipendentemente dal fatto che la frase sia completa o meno.
# è necessario quindi dare delle istruzioni chiare sulla lunghezza della risposta desiderata.
# Ad esempio, si può chiedere esplicitamente di rispondere in un certo numero di parole o frasi.
# %%
QUERY = "Descrivi in modo dettagliato cosa fa un computer."
response = client.chat.completions.create(
    model="gemma3:12b",
    messages=[{"role": "user", "content": QUERY}],
    max_tokens=12
)
print('------------------------------')
print(f"{QUERY}")
print("\nRisposta con max_tokens=12:")
print(response.choices[0].message.content)


# %%
