import json
import random

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider

# Definiamo il modello di chat utilizzando il provider Ollama
ollama_model = OpenAIChatModel(
    model_name='PetrosStav/gemma3-tools:12b',
    provider=OllamaProvider(base_url='http://130.251.104.214:11434/v1'),
)

# Creiamo un agente con il modello definito
agent = Agent(model=ollama_model, system_prompt="Sei un assistente utile che sa fare le somme.")

# Definiamo un semplice tool che somma due numeri
# il tool viene assegnato all'agente tramite il decoratore @agent.tool_plain()
# usiamo tool_plain per semplicità, nel caso dovessimo gestire un contesto 
# potremmo usare @agent.tool (vedi guida pydantic-ai)
@agent.tool_plain()
def add_numbers(a: float, b: float) -> float:   # le annotazioni vengono usate per definire i parametri del tool
    """Somma due numeri."""                     # docstring usata per la descrizione del tool 
    print(f"*** Eseguo il tool add_numbers con a={a} e b={b} ***")
    return a + b

A = random.randint(1, 10)
B = random.randint(1, 10)
C = random.randint(1, 10)
PROMPT = f"Per favore somma {A}, {B} e {C}."

print("\n=== Prompt iniziale ===")
print(f"{PROMPT}")
# Esempio di utilizzo dell'agente
# l'agente eseguirà il suo loop interno, chiamando il tool se necessario ed infine restituendo la risposta
# usiamo "run_sync" per semplicità, pydantic-ai supporta anche l'esecuzione in ambiente asincrono
result = agent.run_sync(PROMPT)

print("\n=== Risultato finale ===")
print(f"{result.output}")  # Stampa la risposta dell'agente

print("\n=== Dettagli esecuzione ===")
# stampiamo quanti token sono stati usati
print(f"{result.usage()}")

# stampiamo il log delle azioni dell'agente
print("\n=== Log delle azioni dell'agente ===")
for idx, message in enumerate(result.all_messages()):
    print(f"\nMessaggio {idx}. Tipo: {message.kind}")
    for part in message.parts:
        if part.part_kind == "tool-call" or part.part_kind == "builtin-tool-call":
            print(f"\t - {part.part_kind}: args: {part.args}")
        else:
            print(f"\t - {part.part_kind}: {part.content}")     


