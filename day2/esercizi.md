# Esercizi: AI agentica

# Esercizio 1: creare un agente AI colloquiale

Crea un agente AI con un loop e message history (vedi <https://ai.pydantic.dev/message-history/#accessing-messages-from-results:~:text=run%20main)-,Using,-Messages%20as%20Input>).

Aggiungi dei tool a tua scelta che possano essere utili per rispondere a domande generiche (esempio: data e ora correnti, calcoli matematici, list di file da disco, lettura files...).

Decidi se implementare il loop come un sistema single agent o multi agent con delegation.


# Esercizio 2: aggiungere memes contestuali alle email di supporto

Aggiungi all'esempio nel file lezione3_pydanticai_multiagente.py la selezione di un meme adeguato al contesto dell'email nella risposta dell'agente.

Trovate le funzioni utili per ottenere i meme da imgflip nel file meme_utils.py.

L'agente dovrà individuare il meme più adeguato al contesto dell'email ricevuta e includere il link del meme nella email di conferma inviata all'utente.

Bonus point: generare delle caption custom compatibili con il template del meme!
