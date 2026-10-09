[English](../../en/05-stm32f103/gps-parse-output.md) | [Deutsch](../../de/05-stm32f103/gps-parse-output.md) | Español | [Français](../../fr/05-stm32f103/gps-parse-output.md) | [Italiano](../../it/05-stm32f103/gps-parse-output.md) | [日本語](../../ja/05-stm32f103/gps-parse-output.md) | [한국어](../../ko/05-stm32f103/gps-parse-output.md) | [Português (BR)](../../pt-br/05-stm32f103/gps-parse-output.md) | [Português (PT)](../../pt-pt/05-stm32f103/gps-parse-output.md) | [简体中文](../../zh-hans/05-stm32f103/gps-parse-output.md) | [繁體中文](../../zh-hant/05-stm32f103/gps-parse-output.md)

**Análisis y salida de datos GPS (STM32)**

**1. Objetivos**

En esta lección utilizamos un STM32F103C8T6 y el módulo GPS para analizar y mostrar la información de posición.

**2. Preparación**

El módulo GPS se comunica por UART y por USB. Aquí usamos el UART del STM32: conecta el TXD del módulo al pin PA10 de la placa STM32F103C8T6, y VCC y GND a los 5 V y GND de la placa. Conecta el GND y el RXD del adaptador TTL al GND y al PA9 del STM32.

![cableado](../../en/05-stm32f103/images/1.png)

**3. Programa**

La velocidad en baudios del módulo es 9600.

![código](../../en/05-stm32f103/images/2.jpg)

Lee y analiza los datos entrantes.

![código](../../en/05-stm32f103/images/3.jpg)

Convierte las unidades de latitud / longitud a grados.

![código](../../en/05-stm32f103/images/4.jpg)

Imprime por el puerto serie los datos recibidos.

![código](../../en/05-stm32f103/images/5.jpg)

Nota: la latitud y la longitud de GPS / BeiDou no guardan una relación simple de ×100; necesitan una conversión de grados y minutos. Por ejemplo, para la latitud `2429.53531` N y la longitud `11810.78036` E:

```
24 + (29.53531 / 60) ≈ 24.49225517
118 + (10.78036 / 60) ≈ 118.17967267
```

Distintos microcontroladores también pueden introducir un pequeño error debido a la precisión de la conversión de datos.

**4. Resultado**

Tras el encendido, el módulo necesita unos 32 s para arrancar; a partir de ahí, el LED de estado de serie parpadea de forma continua y los datos pueden recibirse con normalidad.

Descarga y ejecuta el programa, abre un terminal serie a 9600 baudios y la información de posición actual se imprimirá en bucle.

![salida serie](../../en/05-stm32f103/images/6.jpg)

Ten en cuenta que la antena del módulo debe estar en el exterior; de lo contrario, puede que no adquiera señal GPS.
