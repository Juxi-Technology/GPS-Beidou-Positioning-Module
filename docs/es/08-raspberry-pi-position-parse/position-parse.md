[English](../../en/08-raspberry-pi-position-parse/position-parse.md) | [Deutsch](../../de/08-raspberry-pi-position-parse/position-parse.md) | Español | [Français](../../fr/08-raspberry-pi-position-parse/position-parse.md) | [Italiano](../../it/08-raspberry-pi-position-parse/position-parse.md) | [日本語](../../ja/08-raspberry-pi-position-parse/position-parse.md) | [한국어](../../ko/08-raspberry-pi-position-parse/position-parse.md) | [Português (BR)](../../pt-br/08-raspberry-pi-position-parse/position-parse.md) | [Português (PT)](../../pt-pt/08-raspberry-pi-position-parse/position-parse.md) | [简体中文](../../zh-hans/08-raspberry-pi-position-parse/position-parse.md) | [繁體中文](../../zh-hant/08-raspberry-pi-position-parse/position-parse.md)

**Lectura y análisis de datos de posición GPS (Raspberry Pi)**

**1. Objetivos**

En esta lección utilizamos una Raspberry Pi y el módulo GPS para leer y analizar la información de posición.

**2. Preparación**

El módulo GPS admite comunicación por UART o por USB; aquí usamos USB.

![módulo](../../en/08-raspberry-pi-position-parse/images/1.png)

Conecta la Raspberry Pi al módulo GPS con un cable Type-C y ejecuta `ls /dev | grep 'ttyUSB'`: el módulo se detecta como `USB0`.

![detección del dispositivo](../../en/08-raspberry-pi-position-parse/images/2.jpg)

**3. Programa**

El programa de esta lección es `GPS.py`.

Inicializa el USB:

![código](../../en/08-raspberry-pi-position-parse/images/3.jpg)

La función de adquisición y análisis de posición filtra los datos entrantes en busca de sentencias que empiezan por `GNGGA` y las analiza para volcarlas en variables globales.

![código](../../en/08-raspberry-pi-position-parse/images/4.jpg)

![código](../../en/08-raspberry-pi-position-parse/images/5.jpg)

Con el mismo enfoque se lee y analiza la información de rumbo procedente de `GNVTG`.

![código](../../en/08-raspberry-pi-position-parse/images/6.jpg)

Los datos analizados se imprimen en bucle.

![código](../../en/08-raspberry-pi-position-parse/images/7.jpg)

**4. Ejecución del programa**

Ejecuta `sudo python2 GPS.py` en un terminal.

**5. Resultado**

Tras el encendido, el módulo necesita unos 32 s para arrancar; a partir de ahí, el LED de estado de serie parpadea de forma continua y los datos pueden recibirse con normalidad.

Cuando el programa arranca, inicializa el USB e imprime `GPS Serial Opened! Baudrate=9600` si tiene éxito, o `GPS Serial Open Failed!` si falla; en ese caso, comprueba el cableado o el puerto USB. A continuación imprime la información de posición y de rumbo en bucle.

![salida](../../en/08-raspberry-pi-position-parse/images/8.jpg)

Pulsa Ctrl+C para detener la lectura.

Ten en cuenta que la antena del módulo debe estar en el exterior; de lo contrario, puede que no adquiera señal GPS: cuando no se encuentra señal, se imprime `GPS no found`.
