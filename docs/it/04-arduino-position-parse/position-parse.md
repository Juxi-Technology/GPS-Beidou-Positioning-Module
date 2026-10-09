[English](../../en/04-arduino-position-parse/position-parse.md) | [Deutsch](../../de/04-arduino-position-parse/position-parse.md) | [Español](../../es/04-arduino-position-parse/position-parse.md) | [Français](../../fr/04-arduino-position-parse/position-parse.md) | Italiano | [日本語](../../ja/04-arduino-position-parse/position-parse.md) | [한국어](../../ko/04-arduino-position-parse/position-parse.md) | [Português (BR)](../../pt-br/04-arduino-position-parse/position-parse.md) | [Português (PT)](../../pt-pt/04-arduino-position-parse/position-parse.md) | [简体中文](../../zh-hans/04-arduino-position-parse/position-parse.md) | [繁體中文](../../zh-hant/04-arduino-position-parse/position-parse.md)

**Analisi dei dati di posizione GPS**

**1. Obiettivi**

In questa lezione utilizziamo un Arduino e il modulo GPS per analizzare le informazioni di posizione e stamparle.

**2. Preparazione**

Il modulo GPS comunica tramite UART e USB. Qui utilizziamo la UART dell'Arduino UNO: collegare il TX del modulo al pin D0 dell'UNO, e VCC e GND a 5 V e GND.

![cablaggio](../../en/04-arduino-position-parse/images/1.png)

**3. Programma**

Inizializzare la porta seriale.

![codice](../../en/04-arduino-position-parse/images/2.jpg)

Leggere i dati seriali.

![codice](../../en/04-arduino-position-parse/images/3.jpg)

Analizzare i dati seriali.

![codice](../../en/04-arduino-position-parse/images/4.jpg)

Stampare le informazioni di posizione analizzate.

![codice](../../en/04-arduino-position-parse/images/5.jpg)

**4. Compilazione e caricamento**

4.1 Aprire il file nell'IDE Arduino, fare clic sul pulsante "✓" per compilare, e attendere "Done compiling".

![compilazione](../../en/04-arduino-position-parse/images/6.jpg)

4.2 Nel menu, selezionare Tools → Port → la porta mostrata in Gestione dispositivi.

![selezione della porta](../../en/04-arduino-position-parse/images/7.jpg)

4.3 Fare clic sul pulsante "→" per caricare. Quando compare "Done uploading", il caricamento è riuscito.

![caricamento](../../en/04-arduino-position-parse/images/8.jpg)

**5. Risultato**

Dopo l'accensione il modulo impiega circa 32 s per avviarsi; dopodiché il LED di stato della seriale lampeggia continuamente e i dati possono essere ricevuti normalmente.

Eseguire il programma, aprire il monitor seriale a 9600 baud, e le informazioni di posizione in tempo reale analizzate vengono stampate in un ciclo continuo.

![output seriale](../../en/04-arduino-position-parse/images/9.jpg)

Nota: l'antenna del modulo deve trovarsi all'aperto, altrimenti potrebbe non acquisire il segnale GPS.
