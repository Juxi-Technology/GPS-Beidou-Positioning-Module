English | [简体中文](position-read_CN.md)

**Reading GPS Position Data**

**1. Objectives**

In this lesson we use an Arduino and the GPS module to read position information.

**2. Preparation**

The GPS module communicates over UART and USB. Here we use the Arduino UNO's UART: connect the module's TX to the UNO's D0 pin, and VCC and GND to 5 V and GND.

![wiring](1.png)

**3. Program**

Initialise the serial port.

![code](2.jpg)

Print the received data.

**4. Compile and upload**

4.1 Open the file in the Arduino IDE, click the "✓" button in the toolbar to compile, and wait for "Done compiling" in the status bar.

![compile](3.jpg)

4.2 In the Arduino IDE menu, select Tools → Port → the port shown in Device Manager, as below.

![port selection](4.jpg)

4.3 Then click the "→" button to upload the code to the UNO board. When "Done uploading" appears, the upload succeeded.

![upload](5.jpg)

**5. Result**

After power-up the module needs about 32 s to start; after that the serial status LED blinks continuously and data can be received normally.

Run the program, open the serial monitor and set the baud rate to 9600. The current position information is printed in a loop. This is raw, unprocessed data — see the [CASIC GNSS protocol specification](../../../docs/datasheets/CASIC-GNSS-protocol-spec-CN.pdf) for the meaning of each sentence.

![serial output](6.jpg)

Note that the module's antenna must be outdoors, otherwise it may not acquire a GPS signal.
