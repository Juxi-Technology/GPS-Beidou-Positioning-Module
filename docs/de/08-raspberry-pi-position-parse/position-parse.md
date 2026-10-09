[English](../../en/08-raspberry-pi-position-parse/position-parse.md) | Deutsch | [Español](../../es/08-raspberry-pi-position-parse/position-parse.md) | [Français](../../fr/08-raspberry-pi-position-parse/position-parse.md) | [Italiano](../../it/08-raspberry-pi-position-parse/position-parse.md) | [日本語](../../ja/08-raspberry-pi-position-parse/position-parse.md) | [한국어](../../ko/08-raspberry-pi-position-parse/position-parse.md) | [Português (BR)](../../pt-br/08-raspberry-pi-position-parse/position-parse.md) | [Português (PT)](../../pt-pt/08-raspberry-pi-position-parse/position-parse.md) | [简体中文](../../zh-hans/08-raspberry-pi-position-parse/position-parse.md) | [繁體中文](../../zh-hant/08-raspberry-pi-position-parse/position-parse.md)

**GPS-Positionsdaten lesen und auswerten (Raspberry Pi)**

**1. Ziele**

In dieser Lektion verwenden wir einen Raspberry Pi und das GPS-Modul, um Positionsinformationen zu lesen und auszuwerten.

**2. Vorbereitung**

Das GPS-Modul unterstützt Kommunikation über UART oder USB; hier verwenden wir USB.

![Modul](../../en/08-raspberry-pi-position-parse/images/1.png)

Verbinden Sie den Raspberry Pi mit einem Type-C-Kabel mit dem GPS-Modul und führen Sie dann `ls /dev | grep 'ttyUSB'` aus — das Modul wird als `USB0` erkannt.

![Geräteerkennung](../../en/08-raspberry-pi-position-parse/images/2.jpg)

**3. Programm**

Das Programm für diese Lektion ist `GPS.py`.

USB initialisieren:

![Code](../../en/08-raspberry-pi-position-parse/images/3.jpg)

Die Funktion zum Erfassen und Auswerten der Position filtert die eingehenden Daten nach Sätzen, die mit `GNGGA` beginnen, und wertet sie in globale Variablen aus.

![Code](../../en/08-raspberry-pi-position-parse/images/4.jpg)

![Code](../../en/08-raspberry-pi-position-parse/images/5.jpg)

Auf dieselbe Weise werden die Kursinformationen aus `GNVTG` gelesen und ausgewertet.

![Code](../../en/08-raspberry-pi-position-parse/images/6.jpg)

Die ausgewerteten Daten werden in einer Schleife ausgegeben.

![Code](../../en/08-raspberry-pi-position-parse/images/7.jpg)

**4. Programm ausführen**

Führen Sie `sudo python2 GPS.py` in einem Terminal aus.

**5. Ergebnis**

Nach dem Einschalten benötigt das Modul etwa 32 s, um zu starten; danach blinkt die serielle Status-LED kontinuierlich und Daten können normal empfangen werden.

Beim Start initialisiert das Programm USB und gibt bei Erfolg `GPS Serial Opened! Baudrate=9600` aus, bei Fehlschlag `GPS Serial Open Failed!` — schlägt es fehl, prüfen Sie die Verkabelung oder den USB-Port. Anschließend gibt es Positions- und Kursinformationen in einer Schleife aus.

![Ausgabe](../../en/08-raspberry-pi-position-parse/images/8.jpg)

Drücken Sie Ctrl+C, um das Lesen zu beenden.

Beachten Sie, dass die Antenne des Moduls im Freien angebracht sein muss, da sonst möglicherweise kein GPS-Signal empfangen wird — wird kein Signal gefunden, gibt es `GPS no found` aus.
