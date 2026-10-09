[English](../../en/04-arduino-position-parse/position-parse.md) | [Deutsch](../../de/04-arduino-position-parse/position-parse.md) | Español | [Français](../../fr/04-arduino-position-parse/position-parse.md) | [Italiano](../../it/04-arduino-position-parse/position-parse.md) | [日本語](../../ja/04-arduino-position-parse/position-parse.md) | [한국어](../../ko/04-arduino-position-parse/position-parse.md) | [Português (BR)](../../pt-br/04-arduino-position-parse/position-parse.md) | [Português (PT)](../../pt-pt/04-arduino-position-parse/position-parse.md) | [简体中文](../../zh-hans/04-arduino-position-parse/position-parse.md) | [繁體中文](../../zh-hant/04-arduino-position-parse/position-parse.md)

**Análisis de datos de posición GPS**

**1. Objetivos**

En esta lección utilizamos un Arduino y el módulo GPS para analizar la información de posición e imprimirla.

**2. Preparación**

El módulo GPS se comunica por UART y por USB. Aquí usamos el UART del Arduino UNO: conecta el TX del módulo al pin D0 del UNO, y VCC y GND a 5 V y GND.

![cableado](../../en/04-arduino-position-parse/images/1.png)

**3. Programa**

Inicializa el puerto serie.

![código](../../en/04-arduino-position-parse/images/2.jpg)

Lee los datos del puerto serie.

![código](../../en/04-arduino-position-parse/images/3.jpg)

Analiza los datos del puerto serie.

![código](../../en/04-arduino-position-parse/images/4.jpg)

Imprime la información de posición analizada.

![código](../../en/04-arduino-position-parse/images/5.jpg)

**4. Compilar y cargar**

4.1 Abre el archivo en el IDE de Arduino, haz clic en el botón «✓» para compilar y espera a que aparezca «Done compiling».

![compilar](../../en/04-arduino-position-parse/images/6.jpg)

4.2 En el menú, selecciona Tools → Port → el puerto que aparece en el Administrador de dispositivos.

![selección de puerto](../../en/04-arduino-position-parse/images/7.jpg)

4.3 Haz clic en el botón «→» para cargar. Cuando aparezca «Done uploading», la carga se habrá realizado correctamente.

![cargar](../../en/04-arduino-position-parse/images/8.jpg)

**5. Resultado**

Tras el encendido, el módulo necesita unos 32 s para arrancar; a partir de ahí, el LED de estado de serie parpadea de forma continua y los datos pueden recibirse con normalidad.

Ejecuta el programa, abre el monitor serie a 9600 baudios y la información de posición analizada en tiempo real se imprime en bucle.

![salida serie](../../en/04-arduino-position-parse/images/9.jpg)

Ten en cuenta que la antena del módulo debe estar en el exterior; de lo contrario, puede que no adquiera señal GPS.
