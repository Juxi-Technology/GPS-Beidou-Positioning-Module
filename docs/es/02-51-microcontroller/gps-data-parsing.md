[English](../../en/02-51-microcontroller/gps-data-parsing.md) | [Deutsch](../../de/02-51-microcontroller/gps-data-parsing.md) | Español | [Français](../../fr/02-51-microcontroller/gps-data-parsing.md) | [Italiano](../../it/02-51-microcontroller/gps-data-parsing.md) | [日本語](../../ja/02-51-microcontroller/gps-data-parsing.md) | [한국어](../../ko/02-51-microcontroller/gps-data-parsing.md) | [Português (BR)](../../pt-br/02-51-microcontroller/gps-data-parsing.md) | [Português (PT)](../../pt-pt/02-51-microcontroller/gps-data-parsing.md) | [简体中文](../../zh-hans/02-51-microcontroller/gps-data-parsing.md) | [繁體中文](../../zh-hant/02-51-microcontroller/gps-data-parsing.md)

**Análisis de datos GPS**

**1. Objetivos**

En esta lección utilizamos un microcontrolador STC89C52RC (8051) junto con el módulo GPS para analizar la información de posición.

**2. Preparación**

El módulo GPS se comunica por UART y por USB. Aquí lo leemos a través del UART del 8051: conecta el TX del módulo al pin P3.0 de la placa 8051, y VCC y GND a 5 V y GND.

![cableado](../../en/02-51-microcontroller/images/1.png)

**3. Programa**

Inicializa el puerto serie y el array de datos.

![código](../../en/02-51-microcontroller/images/2.jpg)

Lee y analiza los datos entrantes.

![código](../../en/02-51-microcontroller/images/3.jpg)

Imprime por el puerto serie los datos recibidos.

![código](../../en/02-51-microcontroller/images/4.jpg)

**4. Resultado**

Tras el encendido, el módulo necesita unos 32 s para arrancar; a partir de ahí, el LED de estado de serie parpadea de forma continua y los datos pueden recibirse con normalidad.

Descarga y ejecuta el programa, abre un terminal serie a 9600 baudios y la información de posición actual se imprimirá en bucle.

![salida serie](../../en/02-51-microcontroller/images/5.jpg)

Ten en cuenta que la antena del módulo debe estar en el exterior; de lo contrario, puede que no adquiera señal GPS.
