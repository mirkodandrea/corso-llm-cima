# Giorno 1 – Esercizi: Introduzione all’uso dell’API OpenAI

Obiettivo generale: Prendere confidenza con l’uso programmatico dell’API OpenAI attraverso una serie di esercizi progressivi.

Provate ad utilizzare i vari modelli per i diversi task, variando parametri come temperatura, max tokens, top_p, ecc. per osservare come questi influenzano i risultati e trovare le soluzioni più adatte ai diversi compiti.

## Esercizio 1 – Riassunti in batch

Scrivi uno script che:

- Carichi i file dalla lista di abstract fornita.
- Produca un riassunto di massimo due frasi per ogni testo.
- Generi un riassunto dei riassunti prodotti, con uno stile divulgativo.

## Esercizio 2 – Estrazione di keyword

Costruisci una tabella associativa che mappi ogni articolo con un set di parole chiave rappresentative.
Scrivi uno script che:

- Carichi i file dalla lista di abstract fornita.
- Per ogni testo, chieda al modello di estrarre 3 keyword rappresentative, riutilizzando quando possibile quelle già generate per gli articoli già processati.
- Specifica che l’output deve essere un array di stringhe, tutte in minuscolo, senza testo aggiuntivo: esempio: `["keyword-one", "keyword-two", "keyword-three"]`.
- Associa ogni articolo con le keyword estratte in un dizionario.
- Salva i risultati in un file JSON.

## Esercizio 3 – Estrazione di informazioni dai documenti

Utilizza le keyword estratte nell’esercizio precedente come un semplice corpus di conoscenza per rispondere a domande dell’utente.

Scrivi uno script che:

- Riceva una domanda dell’utente.
- Chieda al modello di selezionare un piccolo insieme (es. 3) di keyword rilevanti per rispondere alla query dal corpus creato nell’esercizio 2.
- Recuperi gli abstract corrispondenti alle keyword selezionate.
- Inoltri questi testi a una successiva chiamata all’API per ottenere la risposta finale basata sui contenuti pertinenti.

## Esercizio 4 – Monitor di allucinazioni

A partire dall’esercizio 3 realizzare un sistema che valuti la bontà delle risposte generate dal modello.

- Analizzi la risposta generata e i riferimenti utilizzati.
- Indichi se il modello ha introdotto informazioni non presenti nei testi di partenza.
- Fornisca un punteggio di affidabilità della risposta (es. da 1 a 10) ed evidenzi eventuali parti allucinate.
