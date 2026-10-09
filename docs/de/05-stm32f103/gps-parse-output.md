[English](../../en/05-stm32f103/gps-parse-output.md) | Deutsch | [Español](../../es/05-stm32f103/gps-parse-output.md) | [Français](../../fr/05-stm32f103/gps-parse-output.md) | [Italiano](../../it/05-stm32f103/gps-parse-output.md) | [日本語](../../ja/05-stm32f103/gps-parse-output.md) | [한국어](../../ko/05-stm32f103/gps-parse-output.md) | [Português (BR)](../../pt-br/05-stm32f103/gps-parse-output.md) | [Português (PT)](../../pt-pt/05-stm32f103/gps-parse-output.md) | [简体中文](../../zh-hans/05-stm32f103/gps-parse-output.md) | [繁體中文](../../zh-hant/05-stm32f103/gps-parse-output.md)

**GPS-Daten auswerten und ausgeben (STM32)**

**1. Ziele**

In dieser Lektion verwenden wir einen STM32F103C8T6 und das GPS-Modul, um Positionsinformationen auszuwerten und auszugeben.

**2. Vorbereitung**

Das GPS-Modul kommuniziert über UART und USB. Hier verwenden wir den UART des STM32: Verbinden Sie den TXD des Moduls mit Pin PA10 der Platine STM32F103C8T6 und VCC sowie GND mit 5 V und GND der Platine. Verbinden Sie GND und RXD des TTL-Adapters mit GND und PA9 des STM32.

![Verkabelung](../../en/05-stm32f103/images/1.png)

**3. Programm**

Die Baudrate des Moduls beträgt 9600.

![Code](../../en/05-stm32f103/images/2.jpg)

Lesen und werten Sie die eingehenden Daten aus.

![Code](../../en/05-stm32f103/images/3.jpg)

Rechnen Sie die Einheiten von Breiten- und Längengrad in Grad um.

![Code](../../en/05-stm32f103/images/4.jpg)

Geben Sie die empfangenen Daten über die serielle Schnittstelle aus.

![Code](../../en/05-stm32f103/images/5.jpg)

Hinweis: Breiten- und Längengrad von GPS / BeiDou stehen nicht in einem einfachen ×100-Verhältnis — sie erfordern eine Umrechnung von Grad und Minuten. Zum Beispiel für den Breitengrad `2429.53531` N und den Längengrad `11810.78036` E:

```
24 + (29.53531 / 60) ≈ 24.49225517
118 + (10.78036 / 60) ≈ 118.17967267
```

Verschiedene Mikrocontroller können aufgrund der Genauigkeit bei der Datenumrechnung außerdem einen kleinen Fehler einführen.

**4. Ergebnis**

Nach dem Einschalten benötigt das Modul etwa 32 s, um zu starten; danach blinkt die serielle Status-LED kontinuierlich und Daten können normal empfangen werden.

Laden Sie das Programm herunter und führen Sie es aus, öffnen Sie ein serielles Terminal mit 9600 Baud, und die aktuelle Positionsinformation wird in einer Schleife ausgegeben.

![serielle Ausgabe](../../en/05-stm32f103/images/6.jpg)

Beachten Sie, dass die Antenne des Moduls im Freien angebracht sein muss, da sonst möglicherweise kein GPS-Signal empfangen wird.
