[English](../../en/03-arduino-position-read/position-read.md) | [Deutsch](../../de/03-arduino-position-read/position-read.md) | Español | [Français](../../fr/03-arduino-position-read/position-read.md) | [Italiano](../../it/03-arduino-position-read/position-read.md) | [日本語](../../ja/03-arduino-position-read/position-read.md) | [한국어](../../ko/03-arduino-position-read/position-read.md) | [Português (BR)](../../pt-br/03-arduino-position-read/position-read.md) | [Português (PT)](../../pt-pt/03-arduino-position-read/position-read.md) | [简体中文](../../zh-hans/03-arduino-position-read/position-read.md) | [繁體中文](../../zh-hant/03-arduino-position-read/position-read.md)

**Lectura de datos de posición GPS**

**1. Objetivos**

En esta lección utilizamos un Arduino y el módulo GPS para leer la información de posición.

**2. Preparación**

El módulo GPS se comunica por UART y por USB. Aquí usamos el UART del Arduino UNO: conecta el TX del módulo al pin D0 del UNO, y VCC y GND a 5 V y GND.

![cableado](../../en/03-arduino-position-read/images/1.png)

**3. Programa**

Inicializa el puerto serie.

![código](../../en/03-arduino-position-read/images/2.jpg)

Imprime los datos recibidos.

**4. Compilar y cargar**

4.1 Abre el archivo en el IDE de Arduino, haz clic en el botón «✓» de la barra de herramientas para compilar y espera a que aparezca «Done compiling» en la barra de estado.

![compilar](../../en/03-arduino-position-read/images/3.jpg)

4.2 En el menú del IDE de Arduino, selecciona Tools → Port → el puerto que aparece en el Administrador de dispositivos, como se muestra a continuación.

![selección de puerto](../../en/03-arduino-position-read/images/4.jpg)

4.3 Después haz clic en el botón «→» para cargar el código en la placa UNO. Cuando aparezca «Done uploading», la carga se habrá realizado correctamente.

![cargar](../../en/03-arduino-position-read/images/5.jpg)

**5. Resultado**

Tras el encendido, el módulo necesita unos 32 s para arrancar; a partir de ahí, el LED de estado de serie parpadea de forma continua y los datos pueden recibirse con normalidad.

Ejecuta el programa, abre el monitor serie y ajusta la velocidad en baudios a 9600. La información de posición actual se imprime en bucle. Se trata de datos sin procesar; consulta la [especificación del protocolo CASIC GNSS](../../../docs/datasheets/CASIC-GNSS-protocol-spec-CN.pdf) para saber qué significa cada sentencia.

![salida serie](../../en/03-arduino-position-read/images/6.jpg)

Ten en cuenta que la antena del módulo debe estar en el exterior; de lo contrario, puede que no adquiera señal GPS.
