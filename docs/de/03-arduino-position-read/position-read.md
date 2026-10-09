[English](../../en/03-arduino-position-read/position-read.md) | Deutsch | [Español](../../es/03-arduino-position-read/position-read.md) | [Français](../../fr/03-arduino-position-read/position-read.md) | [Italiano](../../it/03-arduino-position-read/position-read.md) | [日本語](../../ja/03-arduino-position-read/position-read.md) | [한국어](../../ko/03-arduino-position-read/position-read.md) | [Português (BR)](../../pt-br/03-arduino-position-read/position-read.md) | [Português (PT)](../../pt-pt/03-arduino-position-read/position-read.md) | [简体中文](../../zh-hans/03-arduino-position-read/position-read.md) | [繁體中文](../../zh-hant/03-arduino-position-read/position-read.md)

**GPS-Positionsdaten lesen**

**1. Ziele**

In dieser Lektion verwenden wir einen Arduino und das GPS-Modul, um Positionsinformationen zu lesen.

**2. Vorbereitung**

Das GPS-Modul kommuniziert über UART und USB. Hier verwenden wir den UART des Arduino UNO: Verbinden Sie den TX des Moduls mit Pin D0 des UNO und VCC sowie GND mit 5 V und GND.

![Verkabelung](../../en/03-arduino-position-read/images/1.png)

**3. Programm**

Initialisieren Sie die serielle Schnittstelle.

![Code](../../en/03-arduino-position-read/images/2.jpg)

Geben Sie die empfangenen Daten aus.

**4. Kompilieren und Hochladen**

4.1 Öffnen Sie die Datei in der Arduino IDE, klicken Sie in der Symbolleiste auf die Schaltfläche "✓" zum Kompilieren und warten Sie, bis in der Statusleiste "Done compiling" erscheint.

![Kompilieren](../../en/03-arduino-position-read/images/3.jpg)

4.2 Wählen Sie im Menü der Arduino IDE Werkzeuge → Port → den im Geräte-Manager angezeigten Port, wie unten gezeigt.

![Portauswahl](../../en/03-arduino-position-read/images/4.jpg)

4.3 Klicken Sie dann auf die Schaltfläche "→", um den Code auf die UNO-Platine hochzuladen. Wenn "Done uploading" erscheint, war der Upload erfolgreich.

![Hochladen](../../en/03-arduino-position-read/images/5.jpg)

**5. Ergebnis**

Nach dem Einschalten benötigt das Modul etwa 32 s, um zu starten; danach blinkt die serielle Status-LED kontinuierlich und Daten können normal empfangen werden.

Führen Sie das Programm aus, öffnen Sie den seriellen Monitor und stellen Sie die Baudrate auf 9600 ein. Die aktuelle Positionsinformation wird in einer Schleife ausgegeben. Dies sind unverarbeitete Rohdaten — die Bedeutung der einzelnen Sätze finden Sie in der [CASIC-GNSS-Protokollspezifikation](../../../docs/datasheets/CASIC-GNSS-protocol-spec-CN.pdf).

![serielle Ausgabe](../../en/03-arduino-position-read/images/6.jpg)

Beachten Sie, dass die Antenne des Moduls im Freien angebracht sein muss, da sonst möglicherweise kein GPS-Signal empfangen wird.
