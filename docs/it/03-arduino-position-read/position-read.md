[English](../../en/03-arduino-position-read/position-read.md) | [Deutsch](../../de/03-arduino-position-read/position-read.md) | [Español](../../es/03-arduino-position-read/position-read.md) | [Français](../../fr/03-arduino-position-read/position-read.md) | Italiano | [日本語](../../ja/03-arduino-position-read/position-read.md) | [한국어](../../ko/03-arduino-position-read/position-read.md) | [Português (BR)](../../pt-br/03-arduino-position-read/position-read.md) | [Português (PT)](../../pt-pt/03-arduino-position-read/position-read.md) | [简体中文](../../zh-hans/03-arduino-position-read/position-read.md) | [繁體中文](../../zh-hant/03-arduino-position-read/position-read.md)

**Lettura dei dati di posizione GPS**

**1. Obiettivi**

In questa lezione utilizziamo un Arduino e il modulo GPS per leggere le informazioni di posizione.

**2. Preparazione**

Il modulo GPS comunica tramite UART e USB. Qui utilizziamo la UART dell'Arduino UNO: collegare il TX del modulo al pin D0 dell'UNO, e VCC e GND a 5 V e GND.

![cablaggio](../../en/03-arduino-position-read/images/1.png)

**3. Programma**

Inizializzare la porta seriale.

![codice](../../en/03-arduino-position-read/images/2.jpg)

Stampare i dati ricevuti.

**4. Compilazione e caricamento**

4.1 Aprire il file nell'IDE Arduino, fare clic sul pulsante "✓" nella barra degli strumenti per compilare, e attendere "Done compiling" nella barra di stato.

![compilazione](../../en/03-arduino-position-read/images/3.jpg)

4.2 Nel menu dell'IDE Arduino, selezionare Tools → Port → la porta mostrata in Gestione dispositivi, come riportato di seguito.

![selezione della porta](../../en/03-arduino-position-read/images/4.jpg)

4.3 Fare quindi clic sul pulsante "→" per caricare il codice sulla scheda UNO. Quando compare "Done uploading", il caricamento è riuscito.

![caricamento](../../en/03-arduino-position-read/images/5.jpg)

**5. Risultato**

Dopo l'accensione il modulo impiega circa 32 s per avviarsi; dopodiché il LED di stato della seriale lampeggia continuamente e i dati possono essere ricevuti normalmente.

Eseguire il programma, aprire il monitor seriale e impostare il baud rate su 9600. Le informazioni sulla posizione corrente vengono stampate in un ciclo continuo. Questi sono dati grezzi, non elaborati — vedere la [specifica del protocollo CASIC GNSS](../../../docs/datasheets/CASIC-GNSS-protocol-spec-CN.pdf) per il significato di ciascuna frase.

![output seriale](../../en/03-arduino-position-read/images/6.jpg)

Nota: l'antenna del modulo deve trovarsi all'aperto, altrimenti potrebbe non acquisire il segnale GPS.
