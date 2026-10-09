English | [Deutsch](../../de/02-51-microcontroller/gps-data-parsing.md) | [Español](../../es/02-51-microcontroller/gps-data-parsing.md) | [Français](../../fr/02-51-microcontroller/gps-data-parsing.md) | [Italiano](../../it/02-51-microcontroller/gps-data-parsing.md) | [日本語](../../ja/02-51-microcontroller/gps-data-parsing.md) | [한국어](../../ko/02-51-microcontroller/gps-data-parsing.md) | [Português (BR)](../../pt-br/02-51-microcontroller/gps-data-parsing.md) | [Português (PT)](../../pt-pt/02-51-microcontroller/gps-data-parsing.md) | [简体中文](../../zh-hans/02-51-microcontroller/gps-data-parsing.md) | [繁體中文](../../zh-hant/02-51-microcontroller/gps-data-parsing.md)

**GPS Data Parsing**

**1. Objectives**

In this lesson we use an STC89C52RC (8051) microcontroller together with the GPS module to parse position information.

**2. Preparation**

The GPS module communicates over UART and USB. Here we read it through the 8051's UART: connect the module's TX to pin P3.0 of the 8051 board, and VCC and GND to 5 V and GND.

![wiring](images/1.png)

**3. Program**

Initialise the serial port and the data array.

![code](images/2.jpg)

Read and parse the incoming data.

![code](images/3.jpg)

Print the received data over the serial port.

![code](images/4.jpg)

**4. Result**

After power-up the module needs about 32 s to start; after that the serial status LED blinks continuously and data can be received normally.

Download and run the program, open a serial terminal at 9600 baud, and the current position information is printed in a loop.

![serial output](images/5.jpg)

Note that the module's antenna must be outdoors, otherwise it may not acquire a GPS signal.
