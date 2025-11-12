from openai import OpenAI
from pydantic import BaseModel
from typing import Literal
import json

base_url = "http://130.251.104.214:11434/v1/"
client = OpenAI(api_key="-", base_url=base_url)

class Condimento(BaseModel):
    nome: str
    quantita: str

class Pizza(BaseModel):
    impasto: Literal['base', 'integrale']
    condimenti: list[Condimento]

try:
    response = client.chat.completions.parse(
        model="gemma3:27b",
        temperature=0.0,
        messages=[
            {
                "role": "user",
                "content": "Dammi una lista di ingredienti per una pizza margerita in formato JSON."
            }
        ],
        response_format=Pizza
    )
    response_text = response.choices[0].message
    if response_text.parsed:
        pizza = response_text.parsed

        print(
            f"Pizza con impasto {pizza.impasto} ed i seguenti condimenti: \n"
            + "".join([f"\t - {c.nome} ({c.quantita})\n" for c in pizza.condimenti])
        )

    elif response_text.refusal:
        print(response_text.refusal)
except Exception as e:
    print(f"Error: {e}")
    pizza = Pizza(**json.loads(response_text))                                                                      # type: ignore


