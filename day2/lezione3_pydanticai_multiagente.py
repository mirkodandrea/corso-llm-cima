from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic import BaseModel
from typing import Literal, Annotated

# Definiamo il modello di chat utilizzando il provider Ollama
ollama_model = OpenAIChatModel(
    model_name='gpt-oss:20b',
    provider=OllamaProvider(base_url='http://130.251.104.214:11434/v1'),
)

class SupportTicket(BaseModel):
    tipo_problema: Annotated[str, "Il tipo di problema riscontrato dall'utente."]
    descrizione: Annotated[str, "La descrizione dettagliata del problema."]
    priorita: Annotated[Literal['bassa', 'media', 'alta'], "La priorità del ticket di supporto."]

# Creiamo un agente per il triage dei ticket di supporto
triage_agent = Agent(
    model=ollama_model, 
    system_prompt="Sei un assistente che legge una email di supporto tecnico e produce un ticket strutturato.", 
    output_type=SupportTicket # Specifichiamo il modello di output per questo agente
)

class EventLog(BaseModel):
    tipo_problema: Annotated[str, "Il tipo di problema riscontrato dall'utente."]
    appropriato: Annotated[bool, "Indica se la richiesta è pertinente ai servizi offerti."]
    priorita: Annotated[Literal['bassa', 'media', 'alta'], "La priorità assegnata alla richiesta."]
    evento: Annotated[str, "Descrizione sintetica dell'evento."]
    dettagli: Annotated[str, "Dettagli aggiuntivi sull'evento."]
    email_utente_inviata: Annotated[bool, "Indica se è stata inviata un'email all'utente."] = False
    support_team_notificato: Annotated[bool, "Indica se il team di supporto è stato notificato."] = False

    def __str__(self) -> str:
        return f"""
Log evento:
    evento: {self.evento}
    tipo_problema: {self.tipo_problema}
    appropriato: {self.appropriato}
    priorita: {self.priorita}
    dettagli: {self.dettagli}
    email_utente_inviata: {self.email_utente_inviata}
    support_team_notificato: {self.support_team_notificato}
"""

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
    confirmation_message = f"""Ciao,\n\nAbbiamo ricevuto la tua richiesta di supporto riguardo 
    '{ticket.tipo_problema}'. 
    Il tuo ticket è stato creato con priorità '{ticket.priorita}'. 
    Ti risponderemo al più presto.\n\nGrazie!"""
    # simuliamo l'invio stampando il messaggio
    print(f"""
################### Email di conferma inviata all'utente ###################
{confirmation_message}
###################           Fine email              ###################""")

# definiamo anche un tool per inviare la mail al supporto tecnico interno
@email_agent.tool_plain()
def notify_support_team(ticket: SupportTicket) -> None:
    """Invia una email per notificare il team di supporto tecnico."""
    # in un caso reale qui invieremmo una notifica al team di supporto, per ora simuliamo l'invio
    notification_message = f"""Nuovo ticket di supporto creato:
Tipo: {ticket.tipo_problema}
Descrizione: {ticket.descrizione}
Priorità: {ticket.priorita}"""
    print(f"""
################### Notifica inviata al team di supporto ###################
{notification_message}
###################           Fine notifica              ###################""")


@email_agent.tool_plain()
def send_ignore_email() -> None:
    """Invia una email di risposta per ignorare la richiesta non pertinente."""  
    # in un caso reale qui invieremmo l'email, per ora simuliamo l'invio
    ignore_message = """Ciao,
Grazie per averci contattato. 
Tuttavia, la tua richiesta non riguarda i nostri servizi di supporto tecnico. 
Ti consigliamo di rivolgerti al servizio appropriato.
Grazie!"""
    # simuliamo l'invio stampando il messaggio
    print(f"""
################### Email di risposta per richiesta ignorata ###################
{ignore_message}
###################           Fine email              ###################""")



pertinent_email_text = """
Gentilissimi, buona domenica!

Vi contattiamo per segnalarvi una problematica riscontrata da diverse settimane sulla piattaforma DEWETRA, riguardante il mancato caricamento di diversi layer del gruppo Umidità del suolo. Si tratta di prodotti che, per il Centro Funzionale Decentrato della Regione Sardegna, rivestono un ruolo rilevante nell’attività quotidiana di analisi e redazione del bollettino regionale di criticità. In particolare, risultano attualmente non accessibili i seguenti layer: 

ASCAT_SWI (HSAF)

API-15

API-30

Vi saremmo molto grati se poteste verificare l’origine del disservizio o indicarci eventuali aggiornamenti o modifiche pianificate.

Colgo inoltre l’occasione per chiedere, se possibile, qualche informazione tecnico-scientifica aggiuntiva sul prodotto Soil Moisture (FP Italia), con particolare riferimento alla metodologia di generazione del dato; risoluzione spaziale e temporale; fonti modellistiche e/o satellitari utilizzate; indicazioni operative per una corretta interpretazione.
Vi ringraziamo fin d’ora per il supporto e restiamo a disposizione per eventuali approfondimenti.
Un caro saluto e buon lavoro
"""
result = email_agent.run_sync(pertinent_email_text)
print(result.output)


not_pertinent_email_text = """
Buongiorno,
Vi scrivo per segnalare un problema che sto riscontrando con la mia connessione internet. Da qualche giorno, la velocità di navigazione è notevolmente rallentata e spesso la connessione si interrompe senza motivo apparente. Ho già provato a riavviare il modem e a controllare i cavi, ma il problema persiste.
Vi chiedo gentilmente di verificare la situazione e di fornirmi assistenza per risolvere questo inconveniente.
In attesa di un vostro riscontro, vi ringrazio anticipatamente per l'attenzione.
Cordiali saluti,
Mario Rossi
"""

result = email_agent.run_sync(not_pertinent_email_text)
print(result.output)