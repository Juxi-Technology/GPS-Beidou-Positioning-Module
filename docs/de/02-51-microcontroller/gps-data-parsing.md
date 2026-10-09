[English](../../en/02-51-microcontroller/gps-data-parsing.md) | Deutsch | [Español](../../es/02-51-microcontroller/gps-data-parsing.md) | [Français](../../fr/02-51-microcontroller/gps-data-parsing.md) | [Italiano](../../it/02-51-microcontroller/gps-data-parsing.md) | [日本語](../../ja/02-51-microcontroller/gps-data-parsing.md) | [한국어](../../ko/02-51-microcontroller/gps-data-parsing.md) | [Português (BR)](../../pt-br/02-51-microcontroller/gps-data-parsing.md) | [Português (PT)](../../pt-pt/02-51-microcontroller/gps-data-parsing.md) | [简体中文](../../zh-hans/02-51-microcontroller/gps-data-parsing.md) | [繁體中文](../../zh-hant/02-51-microcontroller/gps-data-parsing.md)

**GPS-Daten auswerten**

**1. Ziele**

In dieser Lektion verwenden wir einen Mikrocontroller STC89C52RC (8051) zusammen mit dem GPS-Modul, um Positionsinformationen auszuwerten.

**2. Vorbereitung**

Das GPS-Modul kommuniziert über UART und USB. Hier lesen wir es über den UART des 8051 aus: Verbinden Sie den TX des Moduls mit Pin P3.0 der 8051-Platine und VCC sowie GND mit 5 V und GND.

![Verkabelung](../../en/02-51-microcontroller/images/1.png)

**3. Programm**

Initialisieren Sie die serielle Schnittstelle und das Daten-Array.

![Code](../../en/02-51-microcontroller/images/2.jpg)

Lesen und werten Sie die eingehenden Daten aus.

![Code](../../en/02-51-microcontroller/images/3.jpg)

Geben Sie die empfangenen Daten über die serielle Schnittstelle aus.

![Code](../../en/02-51-microcontroller/images/4.jpg)

**4. Ergebnis**

Nach dem Einschalten benötigt das Modul etwa 32 s, um zu starten; danach blinkt die serielle Status-LED kontinuierlich und Daten können normal empfangen werden.

Laden Sie das Programm herunter und führen Sie es aus, öffnen Sie ein serielles Terminal mit 9600 Baud, und die aktuelle Positionsinformation wird in einer Schleife ausgegeben.

![serielle Ausgabe](../../en/02-51-microcontroller/images/5.jpg)

Beachten Sie, dass die Antenne des Moduls im Freien angebracht sein muss, da sonst möglicherweise kein GPS-Signal empfangen wird.
