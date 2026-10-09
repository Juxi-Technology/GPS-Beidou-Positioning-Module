[English](../../en/02-51-microcontroller/gps-data-parsing.md) | [Deutsch](../../de/02-51-microcontroller/gps-data-parsing.md) | [Español](../../es/02-51-microcontroller/gps-data-parsing.md) | [Français](../../fr/02-51-microcontroller/gps-data-parsing.md) | Italiano | [日本語](../../ja/02-51-microcontroller/gps-data-parsing.md) | [한국어](../../ko/02-51-microcontroller/gps-data-parsing.md) | [Português (BR)](../../pt-br/02-51-microcontroller/gps-data-parsing.md) | [Português (PT)](../../pt-pt/02-51-microcontroller/gps-data-parsing.md) | [简体中文](../../zh-hans/02-51-microcontroller/gps-data-parsing.md) | [繁體中文](../../zh-hant/02-51-microcontroller/gps-data-parsing.md)

**Analisi dei dati GPS**

**1. Obiettivi**

In questa lezione utilizziamo un microcontrollore STC89C52RC (8051) insieme al modulo GPS per analizzare le informazioni di posizione.

**2. Preparazione**

Il modulo GPS comunica tramite UART e USB. Qui lo leggiamo attraverso la UART dell'8051: collegare il TX del modulo al pin P3.0 della scheda 8051, e VCC e GND a 5 V e GND.

![cablaggio](../../en/02-51-microcontroller/images/1.png)

**3. Programma**

Inizializzare la porta seriale e l'array di dati.

![codice](../../en/02-51-microcontroller/images/2.jpg)

Leggere e analizzare i dati in ingresso.

![codice](../../en/02-51-microcontroller/images/3.jpg)

Stampare i dati ricevuti attraverso la porta seriale.

![codice](../../en/02-51-microcontroller/images/4.jpg)

**4. Risultato**

Dopo l'accensione il modulo impiega circa 32 s per avviarsi; dopodiché il LED di stato della seriale lampeggia continuamente e i dati possono essere ricevuti normalmente.

Scaricare ed eseguire il programma, aprire un terminale seriale a 9600 baud, e le informazioni sulla posizione corrente vengono stampate in un ciclo continuo.

![output seriale](../../en/02-51-microcontroller/images/5.jpg)

Nota: l'antenna del modulo deve trovarsi all'aperto, altrimenti potrebbe non acquisire il segnale GPS.
