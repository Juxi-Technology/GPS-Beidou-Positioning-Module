[English](../../en/04-arduino-position-parse/position-parse.md) | Deutsch | [Español](../../es/04-arduino-position-parse/position-parse.md) | [Français](../../fr/04-arduino-position-parse/position-parse.md) | [Italiano](../../it/04-arduino-position-parse/position-parse.md) | [日本語](../../ja/04-arduino-position-parse/position-parse.md) | [한국어](../../ko/04-arduino-position-parse/position-parse.md) | [Português (BR)](../../pt-br/04-arduino-position-parse/position-parse.md) | [Português (PT)](../../pt-pt/04-arduino-position-parse/position-parse.md) | [简体中文](../../zh-hans/04-arduino-position-parse/position-parse.md) | [繁體中文](../../zh-hant/04-arduino-position-parse/position-parse.md)

**GPS-Positionsdaten auswerten**

**1. Ziele**

In dieser Lektion verwenden wir einen Arduino und das GPS-Modul, um Positionsinformationen auszuwerten und auszugeben.

**2. Vorbereitung**

Das GPS-Modul kommuniziert über UART und USB. Hier verwenden wir den UART des Arduino UNO: Verbinden Sie den TX des Moduls mit Pin D0 des UNO und VCC sowie GND mit 5 V und GND.

![Verkabelung](../../en/04-arduino-position-parse/images/1.png)

**3. Programm**

Initialisieren Sie die serielle Schnittstelle.

![Code](../../en/04-arduino-position-parse/images/2.jpg)

Lesen Sie die seriellen Daten.

![Code](../../en/04-arduino-position-parse/images/3.jpg)

Werten Sie die seriellen Daten aus.

![Code](../../en/04-arduino-position-parse/images/4.jpg)

Geben Sie die ausgewerteten Positionsinformationen aus.

![Code](../../en/04-arduino-position-parse/images/5.jpg)

**4. Kompilieren und Hochladen**

4.1 Öffnen Sie die Datei in der Arduino IDE, klicken Sie auf die Schaltfläche "✓" zum Kompilieren und warten Sie auf "Done compiling".

![Kompilieren](../../en/04-arduino-position-parse/images/6.jpg)

4.2 Wählen Sie im Menü Werkzeuge → Port → den im Geräte-Manager angezeigten Port.

![Portauswahl](../../en/04-arduino-position-parse/images/7.jpg)

4.3 Klicken Sie auf die Schaltfläche "→", um hochzuladen. Wenn "Done uploading" erscheint, war der Upload erfolgreich.

![Hochladen](../../en/04-arduino-position-parse/images/8.jpg)

**5. Ergebnis**

Nach dem Einschalten benötigt das Modul etwa 32 s, um zu starten; danach blinkt die serielle Status-LED kontinuierlich und Daten können normal empfangen werden.

Führen Sie das Programm aus, öffnen Sie den seriellen Monitor mit 9600 Baud, und die ausgewerteten Positionsinformationen in Echtzeit werden in einer Schleife ausgegeben.

![serielle Ausgabe](../../en/04-arduino-position-parse/images/9.jpg)

Beachten Sie, dass die Antenne des Moduls im Freien angebracht sein muss, da sonst möglicherweise kein GPS-Signal empfangen wird.
