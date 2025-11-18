""" Esempio semplice di tool calling usando l'API chat completions """
# %%
from openai import OpenAI
import json
import random
BASE_URL = "http://130.251.104.214:11434/v1/"
DEFAULT_MODEL = "gpt-oss:20b"

client = OpenAI(api_key="LA_TUA_API_KEY", base_url=BASE_URL)
A = random.randint(1, 10)
B = random.randint(1, 10)
PROMPT = f"Per favore somma {A} e {B}."



# Prima definiamo un semplice tool che somma due numeri
def add_numbers(a: float, b: float) -> float:
    """Somma due numeri."""
    return a + b


# Definizione del tool nel formato richiesto dall'API
tool_def = {
    "name": "add_numbers",
    "description": "Somma due numeri.",
    "parameters": {
        "type": "object",
        "properties": {
            "a": {"type": "number", "description": "Il primo numero."},
            "b": {"type": "number", "description": "Il secondo numero."},
        },
        "required": ["a", "b"],
    },
}

# Prepariamo i messaggi con il contesto di sistema e la richiesta dell'utente
messages = [
            {
            "role": "system",
            "content": "Sei un assistente utile. Puoi usare il tool add_numbers per sommare due numeri.",
        },
            {
            "role": "user",
            "content": PROMPT,
        },
]

# Ora chiamiamo l'API chat completions con un prompt che usa il tool
# Prima chiamata al modello passando il tool disponibile
response = client.chat.completions.create(
    model=DEFAULT_MODEL,
    messages=messages,                                                                                                                              # type: ignore  
    tools=[tool_def],                                                                                                                               # type: ignore
)

print(f"Risposta dal modello: {response.choices[0].message.content}") # molto probabilmente vuota, perché il modello chiede di usare il tool
tool_calls = response.choices[0].message.tool_calls # estraiamo le chiamate ai tool! dovrebbbe esserci una chiamata a add_numbers

# Processiamo le chiamate ai tool richieste dal modello
for tool_call in tool_calls:                                                                                                                        # type: ignore  
    print(f"chiamato {tool_call.function.name}")                                                                                                    # type: ignore
    print(f"tool_call.function.arguments: {tool_call.function.arguments}")                                                                          # type: ignore

    # Se il tool chiamato è add_numbers, eseguiamo la somma
    if tool_call.function.name == "add_numbers":                                                                                                    # type: ignore     
        args = json.loads(tool_call.function.arguments)                                                                                             # type: ignore
        a = args["a"]
        b = args["b"]
        result = add_numbers(a, b)
        print(f"Risultato della somma di {a} e {b}: {result}")

    # Aggiungiamo il risultato del tool ai messaggi
    messages.append({
        "role": "tool",                      # il ruolo è "tool" per indicare che questo messaggio è una risposta da un tool
        "tool_call_id": tool_call.id,       # per collegare la risposta al tool call specifico, nel caso di più tool call allo stesso tool
        "content": str(result),             # il risultato del tool come stringa
        "name": tool_call.function.name,                                                                                                           # type: ignore
    })

# Ora inviamo i risultati del tool call al modello per ottenere la risposta finale
response_final = client.chat.completions.create(
    model=DEFAULT_MODEL,
    messages=messages,                                                                                                                              # type: ignore
)
print(f"Risposta finale dal modello: {response_final.choices[0].message.content}")


