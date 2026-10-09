[English](../../en/06-jetson-nano-position-parse/position-parse.md) | [Deutsch](../../de/06-jetson-nano-position-parse/position-parse.md) | [Español](../../es/06-jetson-nano-position-parse/position-parse.md) | [Français](../../fr/06-jetson-nano-position-parse/position-parse.md) | Italiano | [日本語](../../ja/06-jetson-nano-position-parse/position-parse.md) | [한국어](../../ko/06-jetson-nano-position-parse/position-parse.md) | [Português (BR)](../../pt-br/06-jetson-nano-position-parse/position-parse.md) | [Português (PT)](../../pt-pt/06-jetson-nano-position-parse/position-parse.md) | [简体中文](../../zh-hans/06-jetson-nano-position-parse/position-parse.md) | [繁體中文](../../zh-hant/06-jetson-nano-position-parse/position-parse.md)

**Lettura e analisi dei dati di posizione GPS (Jetson)**

**1. Obiettivi**

In questa lezione utilizziamo un Jetson Orin e il modulo GPS per leggere e analizzare le informazioni di posizione.

**2. Preparazione**

Il modulo GPS supporta la comunicazione UART o USB; qui utilizziamo l'USB.

![modulo](../../en/06-jetson-nano-position-parse/images/1.png)

Collegare il Jetson Orin al modulo GPS con un cavo Type-C, quindi eseguire `ls /dev | grep 'ttyUSB'` — il modulo viene rilevato come `USB0`.

![rilevamento del dispositivo](../../en/06-jetson-nano-position-parse/images/2.jpg)

**3. Programma**

Il programma di questa lezione è `GPS.py`.

Inizializzare l'USB:

![codice](../../en/06-jetson-nano-position-parse/images/3.jpg)

La funzione di acquisizione e analisi della posizione filtra i dati in ingresso cercando le frasi che iniziano con `GNGGA` e le analizza in variabili globali.

![codice](../../en/06-jetson-nano-position-parse/images/4.jpg)

![codice](../../en/06-jetson-nano-position-parse/images/5.jpg)

Con lo stesso approccio si leggono e si analizzano le informazioni di rotta da `GNVTG`.

![codice](../../en/06-jetson-nano-position-parse/images/6.jpg)

I dati analizzati vengono stampati in un ciclo continuo.

![codice](../../en/06-jetson-nano-position-parse/images/7.jpg)

**4. Esecuzione del programma**

Eseguire `sudo python3 GPS.py` in un terminale.

**5. Risultato**

Dopo l'accensione il modulo impiega circa 32 s per avviarsi; dopodiché il LED di stato della seriale lampeggia continuamente e i dati possono essere ricevuti normalmente.

All'avvio il programma inizializza l'USB e stampa `GPS Serial Opened! Baudrate=9600` in caso di successo, oppure `GPS Serial Open Failed!` in caso di errore — se fallisce, verificare il cablaggio o la porta USB. Poi stampa in un ciclo continuo le informazioni di posizione e rotta.

![output](../../en/06-jetson-nano-position-parse/images/8.jpg)

Premere Ctrl+C per interrompere la lettura.

![uscita](../../en/06-jetson-nano-position-parse/images/9.jpg)

Nota: l'antenna del modulo deve trovarsi all'aperto, altrimenti potrebbe non acquisire il segnale GPS — quando non viene trovato alcun segnale stampa `GPS no found`.
