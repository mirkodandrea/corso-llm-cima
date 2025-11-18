from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic import BaseModel
from typing import Literal

# Definiamo il modello di chat utilizzando il provider Ollama
ollama_model = OpenAIChatModel(
    model_name='gpt-oss:20b',
    provider=OllamaProvider(base_url='http://130.251.104.214:11434/v1'),
)

class SupportTicket(BaseModel):
    tipo_problema: str
    descrizione: str
    priorita: Literal['bassa', 'media', 'alta']

# Creiamo un agente per il triage dei ticket di supporto
triage_agent = Agent(
    model=ollama_model, 
    system_prompt="Sei un assistente che legge una email di supporto tecnico e produce un ticket strutturato.", 
    output_type=SupportTicket                                                                                                                       # Specifichiamo il modello di output per questo agente
)

class EventLog(BaseModel):
    evento: str
    tipo_problema: str
    appropriato: bool
    priorita: Literal['bassa', 'media', 'alta']
    dettagli: str

# ora definiamo un agente che riceve le email, richiede il triage e risponde all'utente
email_agent = Agent(
    model=ollama_model,
    system_prompt="""
    Sei un assistente che riceve email di richiesta supporto tecnico per gli applicativi webgis ed i dati geografici e meteorologici.
    Se la mail riguarda questi applicativi e dati, esegui la funzione di triage ed invia le comunicazioni all'utente ed al supporto tecnico. 
    Se la mail NON riguarda questi applicativi e dati comunica all'utente che non sei in grado di aiutarlo con l'apposito tool `send_ignore_email`.
    Dopo aver gestito la richiesta, produci un log strutturato dell'evento.
    """,
    output_type=EventLog
)   

# creiamo il tool per il triage che usa l'agente di triage
@email_agent.tool_plain()
def triage_support_email(email_text: str) -> SupportTicket:
    """Esegue il triage di una email di supporto tecnico."""
    # chiamiamo l'agente di triage per ottenere il ticket strutturato
    result = triage_agent.run_sync(email_text)
    ticket = result.output
    return ticket

# definiamo il tool per invio automatico dell'email di risposta
@email_agent.tool_plain()
def send_confirmation_email(ticket: SupportTicket) -> None:
    """Invia una email di conferma all'utente."""  
    # in un caso reale qui invieremmo l'email, per ora simuliamo l'invio
    confirmation_message = f"Ciao,\n\nAbbiamo ricevuto la tua richiesta di supporto riguardo '{ticket.tipo_problema}'. Il tuo ticket è stato creato con priorità '{ticket.priorita}'. Ti risponderemo al più presto.\n\nGrazie!"
    # simuliamo l'invio stampando il messaggio
    print(f"""
################### Email di conferma inviata all'utente ###################
{confirmation_message}
###################           Fine email              ###################""")

# definiamo anche un tool per inviare la mail al supporto tecnico interno
@email_agent.tool_plain()
def notify_support_team(ticket: SupportTicket, original_email_text: str) -> None:
    """Invia una email per notificare il team di supporto tecnico."""
    # in un caso reale qui invieremmo una notifica al team di supporto, per ora simuliamo l'invio
    notification_message = f"Nuovo ticket di supporto creato:\nTipo: {ticket.tipo_problema}\nDescrizione: {ticket.descrizione}\nPriorità: {ticket.priorita}\nEmail originale: {original_email_text}"
    print(f"""
################### Notifica inviata al team di supporto ###################
{notification_message}
###################           Fine notifica              ###################""")


@email_agent.tool_plain()
def send_ignore_email() -> None:
    """Invia una email di risposta per ignorare la richiesta non pertinente."""  
    # in un caso reale qui invieremmo l'email, per ora simuliamo l'invio
    ignore_message = f"Ciao,\n\nGrazie per averci contattato. Tuttavia, la tua richiesta non riguarda i nostri servizi di supporto tecnico per applicativi webgis e dati geografici/meteorologici. Ti consigliamo di rivolgerti al servizio appropriato.\n\nGrazie!"
    # simuliamo l'invio stampando il messaggio
    print(f"""
################### Email di risposta per richiesta ignorata ###################
{ignore_message}
###################           Fine email              ###################""")



# carica le email di supporto da un file txt con separatore '-----'
with open("emails/emails.txt", "r") as f:
    email_texts = f.read().split("-----")

# elaboriamo ogni email
for idx, email_text in enumerate(email_texts[-1:]):
    email_text = email_text.strip()
    if not email_text:
        continue
    print(f"\n=== Elaborazione email {idx+1} ===")
    print(f" <<<<< Email:\n{email_text}\n")
    # Eseguiamo l'agente per ogni email
    result = email_agent.run_sync(email_text)
    print(f"\n >>>> Risultato finale per email {idx+1}")
    print(f"{result.output}")  # Stampa la risposta dell'agente