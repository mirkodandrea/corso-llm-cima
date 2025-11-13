import base64
from openai import OpenAI

# piccola funzione di utilità per convertire un'immagine in base64
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

base_url = "http://130.251.104.214:11434/v1/"
client = OpenAI(api_key="-", base_url=base_url)

# Percorso dell'immagine
image_path = "./cat_meme.png" 

# Immagine codificata in base64
base64_image = encode_image_to_base64(image_path)


# Effettua la chiamata API con l'immagine incorporata nel messaggio
response = client.chat.completions.create(
    model="gemma3:12b",
    temperature=0.7,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Cosa c'è in questa immagine?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}" # incorpora l'immagine in base64
                    }
                }
            ],
        }
    ],
    max_tokens=300,
)

# Stampa la risposta del modello
print(response.choices[0].message.content)
