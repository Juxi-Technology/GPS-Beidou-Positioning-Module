English | [Deutsch](../../de/04-arduino-position-parse/position-parse.md) | [Español](../../es/04-arduino-position-parse/position-parse.md) | [Français](../../fr/04-arduino-position-parse/position-parse.md) | [Italiano](../../it/04-arduino-position-parse/position-parse.md) | [日本語](../../ja/04-arduino-position-parse/position-parse.md) | [한국어](../../ko/04-arduino-position-parse/position-parse.md) | [Português (BR)](../../pt-br/04-arduino-position-parse/position-parse.md) | [Português (PT)](../../pt-pt/04-arduino-position-parse/position-parse.md) | [简体中文](../../zh-hans/04-arduino-position-parse/position-parse.md) | [繁體中文](../../zh-hant/04-arduino-position-parse/position-parse.md)

**Parsing GPS Position Data**

**1. Objectives**

In this lesson we use an Arduino and the GPS module to parse position information and print it.

**2. Preparation**

The GPS module communicates over UART and USB. Here we use the Arduino UNO's UART: connect the module's TX to the UNO's D0 pin, and VCC and GND to 5 V and GND.

![wiring](images/1.png)

**3. Program**

Initialise the serial port.

![code](images/2.jpg)

Read the serial data.

![code](images/3.jpg)

Parse the serial data.

![code](images/4.jpg)

Print the parsed position information.

![code](images/5.jpg)

**4. Compile and upload**

4.1 Open the file in the Arduino IDE, click the "✓" button to compile, and wait for "Done compiling".

![compile](images/6.jpg)

4.2 In the menu, select Tools → Port → the port shown in Device Manager.

![port selection](images/7.jpg)

4.3 Click the "→" button to upload. When "Done uploading" appears, the upload succeeded.

![upload](images/8.jpg)

**5. Result**

After power-up the module needs about 32 s to start; after that the serial status LED blinks continuously and data can be received normally.

Run the program, open the serial monitor at 9600 baud, and the parsed real-time position information is printed in a loop.

![serial output](images/9.jpg)

Note that the module's antenna must be outdoors, otherwise it may not acquire a GPS signal.
