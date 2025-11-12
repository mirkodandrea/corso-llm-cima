# Giorno 1 – Esercizi: Introduzione all’uso dell’API OpenAI

Obiettivo generale: Prendere confidenza con l’uso programmatico dell’API OpenAI attraverso una serie di esercizi progressivi.

Provate ad utilizzare i diversi modelli a disposizione ed i concetti appresi oggi!


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


## Esercizio 5 Bot Indovina CIMA
Realizza un bot che giochi ad indovina chi usando le immagini presenti nella cartella `images/`.
- Carica le immagini dalla cartella `images/`.
- Per ogni immagine, chiedi al modello di generare una descrizione ed un json con le caratteristiche salienti (es. colore dei capelli, occhiali, cappello)
- Implementa un loop di gioco in cui l’utente può fare domande sulle caratteristiche delle immagini per cercare di indovinare quale immagine il bot ha scelto.
- Il bot deve rispondere alle domande basandosi sulle descrizioni e caratteristiche generate in precedenza.
Buon divertimento!