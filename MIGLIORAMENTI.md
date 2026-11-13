# Carta di pesca: possibili modifiche future

Elenco delle idee emerse dopo la versione 18 (novembre 2026), in ordine di utilità stimata.
Nessuna è ancora iniziata. Le prime due sono quelle consigliate per partire.

## 1. Uso senza rete in barca

**Problema.** Senza segnale la app mostra solo l'ultima zona caricata attorno al target; il resto della mappa resta vuoto.

**Idea.** Renderla un'app installabile che tiene in memoria sul telefono:

- la pagina stessa e le librerie che oggi scarica da fuori (mappa, calcoli astronomici, caratteri);
- il rilievo della laguna e il file di canali, barene e strutture, che sono già nel sito;
- le tessere della carta di sfondo per la zona scelta, scaricate in anticipo con un pulsante "Scarica questa zona".

**Da decidere.** Quanta memoria occupare per la carta di sfondo e fino a che zoom. Meteo e marea senza rete restano quelli dell'ultimo caricamento, con la data bene in vista.

## 2. Marea vera di Chioggia

**Problema.** Il livello del mare viene da un modello a 8 km, indicativo. In laguna la marea arriva in ritardo e con altezza diversa rispetto al mare, e da quel numero dipendono i "bassi fondali per la tua barca".

**Idea.** Usare le previsioni del Centro Maree del Comune di Venezia per la stazione più vicina al target (Chioggia, Punta della Salute, Burano e le altre), tenendo il modello attuale come riserva fuori dalla laguna.

**Da verificare.** Se i dati del Centro Maree si possono leggere direttamente da una pagina web e con quali condizioni d'uso.

## 3. Taratura con l'ecoscandaglio

**Problema.** Il rilievo della laguna è riportato al medio mare con uno scarto fisso di 40 cm, scelto per far tornare 1,7 m sui bassifondi di Chioggia. Lo scarto reale può cambiare da zona a zona.

**Idea.** Un pulsante "qui leggo X metri" sul punto toccato o sulla posizione GPS. La app salva la misura con ora e marea, calcola lo scarto rispetto al rilievo e corregge i fondali nei dintorni. Con abbastanza misure lo scarto fisso diventa una correzione per zona.

**Da decidere.** Quanto lontano far valere una misura e come trattare misure in disaccordo tra loro.

## 4. Diario che insegna

**Problema.** Le catture salvate nel diario oggi compaiono solo come punti sulla mappa.

**Idea.** Usarle per alzare il punteggio delle zone e delle condizioni che hanno funzionato: specie, punto, fondale, fase di marea, ora, luce, esca. Mostrare anche un riepilogo: "con marea calante al tramonto hai fatto 6 catture su 9".

**Limite.** Serve un numero minimo di catture prima che il segnale sia affidabile; sotto quella soglia la app deve dirlo e non cambiare i punteggi.

## 5. Rotta lungo i canali

**Problema.** "Portami lì" dà la linea retta verso il punto e avvisa soltanto se attraversa terra o fondali bassi.

**Idea.** Con canali e rilievo ora in memoria, calcolare un percorso che segue i canali e passa solo dove il fondale, con la marea dell'ora scelta, basta per il pescaggio della barca. Mostrare lunghezza, tempo stimato e il punto più basso del percorso.

**Limite.** Resta un aiuto e non una carta nautica: bricole, divieti e limiti di velocità non sono tutti nei dati.

## 6. Corrente nei canali

**Problema.** In laguna il pesce mangia sul giro di corrente, ma la app conosce solo la marea come variazione di livello.

**Idea.** Stimare verso e forza della corrente nei canali principali a partire dalla marea alle bocche di porto (montante entra, calante esce, con ritardo crescente verso l'interno), e usarla sia nelle finestre del Piano sia per dire su quale lato del canale mettersi.

**Limite.** Sarebbe una stima semplificata: senza un modello idrodinamico vero vale per i canali grandi vicino alle bocche, meno per l'interno.

## Note per chi riprende il lavoro

- **Dati nel sito.** Cartella `laguna/`: rilievo della laguna in tre livelli di dettaglio (`0`, `1`, `2`) e `osm.json` con canali, barene, costa e strutture. Sono estratti fatti a novembre 2026 e vanno rigenerati per aggiornarli.
- **Fuori dalla laguna di Venezia** fondali e strutture arrivano ancora dai servizi esterni (EMODnet a 115 m e OpenStreetMap), con i limiti di precisione e di velocità che ne derivano.
- **Non provato su iPhone vero.** Layout e caricamenti sono stati verificati in un browser che simula l'iPhone 17 Pro; il comportamento su Safari va confermato a ogni versione.
- **Licenze.** Il codice è "tutti i diritti riservati"; i dati di terzi mantengono le loro licenze (vedi `LICENSE`).
