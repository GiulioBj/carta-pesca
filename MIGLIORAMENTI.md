# Carta di pesca: possibili modifiche future

Elenco delle idee emerse dopo la versione 18 (novembre 2026). Le voci da 1 a 6 sono in ordine di utilità stimata; quelle da 7 a 11 sono nate con il vento sulla mappa.

**Fatto nella versione 19:** bussola con freccia del vento e dello scarroccio, scie animate del vento con interruttore e trasparenza, installazione come app anche su Android (manifest, icone e service worker).

**Fatto nella versione 20 (previsioni e consigli):**

- limpidezza stimata da vento, mare e pioggia degli ultimi due giorni, distinta tra laguna e mare, con la causa indicata;
- affidabilità della previsione dal confronto tra due modelli meteo sul vento;
- stagione per specie a tre livelli (mese migliore, in stagione, fuori stagione) che tiene conto della temperatura dell'acqua;
- pressione valutata anche sull'andamento delle ultime 24 ore;
- scheda "Perché questo punteggio" nel Piano, con il contributo di ogni voce;
- nella app, tutto il necessario per la marea reale del Centro Maree, la corrente stimata nei canali e la temperatura dell'acqua misurata (vedi voci 2 e 6).

**Non fatto, per scelta:** il diario che corregge i pesi (voce 4) resta per dopo.

**Prossime consigliate:** la 7 e la 8 insieme, perché riusano il calcolo dello scarroccio che c'è già.

## 1. Uso senza rete in barca

**Stato.** Avviato con la versione 19: la app è installabile e, senza rete, riapre la pagina e i file del sito già visitati. Mancano le librerie esterne e le tessere della carta di sfondo.

**Problema.** Senza segnale la app mostra solo l'ultima zona caricata attorno al target; il resto della mappa resta vuoto.

**Idea.** Renderla un'app installabile che tiene in memoria sul telefono:

- la pagina stessa e le librerie che oggi scarica da fuori (mappa, calcoli astronomici, caratteri);
- il rilievo della laguna e il file di canali, barene e strutture, che sono già nel sito;
- le tessere della carta di sfondo per la zona scelta, scaricate in anticipo con un pulsante "Scarica questa zona".

**Da decidere.** Quanta memoria occupare per la carta di sfondo e fino a che zoom. Meteo e marea senza rete restano quelli dell'ultimo caricamento, con la data bene in vista.

## 2. Marea vera di Chioggia

**Problema.** Il livello del mare viene da un modello a 8 km, indicativo. In laguna la marea arriva in ritardo e con altezza diversa rispetto al mare, e da quel numero dipendono i "bassi fondali per la tua barca".

**Idea.** Usare le previsioni del Centro Maree del Comune di Venezia per la stazione più vicina al target (Chioggia, Punta della Salute, Burano e le altre), tenendo il modello attuale come riserva fuori dalla laguna.

**Stato.** La app è pronta dalla versione 20. I dati sono open data con licenza CC BY (dati.venezia.it): previsione ufficiale dei massimi e minimi a Punta Salute per circa tre giorni, marea astronomica per i giorni successivi, livelli misurati ogni 5 minuti in 14 stazioni. Lo script `tools/maree.py` li riunisce in `maree.json` e calcola, dalle misure degli ultimi tre giorni, ritardo e ampiezza di ogni stazione rispetto a Punta Salute. La app usa la stazione più vicina al target (entro 25 km) e corregge la curva con l'ultima misura.

**Da attivare.** Serve l'aggiornamento automatico ogni mezz'ora (`.github/workflows/maree.yml`), che pubblica `maree.json` nel ramo `dati`. Finché non è attivo la app continua con il modello a 8 km. GitHub sospende gli aggiornamenti programmati dopo 60 giorni senza modifiche al repository: basta riattivarli dalla scheda Actions.

**Limiti.** Prima che ci siano abbastanza misure i ritardi delle stazioni sono valori indicativi. Oltre i tre giorni vale la sola marea astronomica, senza l'effetto di vento e pressione.

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

**Stato.** Fatta in forma semplice nella versione 20, attiva insieme alla marea reale: la velocità segue il ritmo con cui cambia il livello ed è più forte vicino alla bocca di porto; montante entra, calante esce. Entra nello scarroccio e nella spiegazione del punteggio.

**Limite.** È una stima semplificata: senza un modello idrodinamico vero vale per i canali grandi vicino alle bocche, meno per l'interno, e non conosce la direzione del singolo canale.

## 7. Passata di scarroccio sulla mappa

**Problema.** La app dice verso e velocità dello scarroccio, ma non mostra dove porta la barca.

**Idea.** Toccando un punto, disegnare la linea che la barca percorre nei 15, 30 e 60 minuti successivi con vento e corrente dell'ora scelta, e i fondali che attraversa. Al contrario, dato uno spot, indicare da dove partire per passarci sopra.

**Limite.** Il vento è quello previsto sul target e la corrente c'è solo dove il modello la fornisce: in canale la deriva reale può essere diversa.

## 8. Cursore delle ore

**Problema.** Per confrontare le ore bisogna aprire ogni volta il menu a tendina.

**Idea.** Una barra da trascinare sotto la mappa: vento, scarroccio, bassi fondali e zone probabili cambiano mentre si scorre, e la finestra buona si trova a colpo d'occhio.

## 9. Zone ridossate

**Problema.** Con vento teso non si capisce subito dove si pesca ancora comodi.

**Idea.** Colorare le acque riparate dal vento dell'ora scelta, cioè quelle con terra, barene, dighe o isole sopravento entro una certa distanza.

**Da decidere.** Quanta distanza sopravento conta come riparo e come trattare le barene sommerse con l'alta marea.

## 10. Vento contro corrente

**Problema.** Alle bocche di porto, con vento e marea in versi opposti, l'onda diventa corta e ripida anche con poco vento.

**Idea.** Un avviso nel Piano e sulla mappa nelle ore in cui vento e corrente sono contrari alle bocche. Dipende dalla stima della corrente della voce 6.

## 11. Allarme ancora

**Problema.** All'ancora, se la barca ara ci si accorge tardi.

**Idea.** Fissare il punto quando si cala l'ancora e far suonare il telefono se la posizione GPS esce da un raggio scelto.

**Limite.** Funziona solo con la app aperta e lo schermo acceso: il browser non segue la posizione in sottofondo.

## Note per chi riprende il lavoro

- **Dati nel sito.** Cartella `laguna/`: rilievo della laguna in tre livelli di dettaglio (`0`, `1`, `2`) e `osm.json` con canali, barene, costa e strutture. Sono estratti fatti a novembre 2026 e vanno rigenerati per aggiornarli.
- **Fuori dalla laguna di Venezia** fondali e strutture arrivano ancora dai servizi esterni (EMODnet a 115 m e OpenStreetMap), con i limiti di precisione e di velocità che ne derivano.
- **Versioni 21-25.** Marea reale attiva (azione ogni mezz'ora, ramo `dati`), orari al minuto con i ritardi pubblicati dal Centro Maree, confronto con le tabelle astronomiche, misure di livello, vento e acqua solo da stazioni vicine al target, freccia del vento sul target, "Oggi" sempre di 24 ore. La rotazione della mappa (v24) e le frecce dello scarroccio su bussola e mappa (v23) sono state tolte nella v25 su richiesta: creavano problemi e non piacevano. Lo scarroccio resta come testo nella scheda Spot.
- **Versione 20 provata solo con dati simulati.** Meteo, marea e misure sono stati simulati nei formati reali; con i dati veri vanno ricontrollati soprattutto orari della marea (ora solare e ora legale) e nome del secondo modello meteo (`gfs_seamless`).
- **Installazione su Android non provata su un telefono vero.** Manifest, icone e service worker sono stati controllati solo in un browser da computer.
- **Non provato su iPhone vero.** Layout e caricamenti sono stati verificati in un browser che simula l'iPhone 17 Pro; il comportamento su Safari va confermato a ogni versione.
- **Licenze.** Il codice è "tutti i diritti riservati"; i dati di terzi mantengono le loro licenze (vedi `LICENSE`).
