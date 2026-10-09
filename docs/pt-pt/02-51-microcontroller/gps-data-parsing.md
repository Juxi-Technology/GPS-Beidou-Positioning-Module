[English](../../en/02-51-microcontroller/gps-data-parsing.md) | [Deutsch](../../de/02-51-microcontroller/gps-data-parsing.md) | [Español](../../es/02-51-microcontroller/gps-data-parsing.md) | [Français](../../fr/02-51-microcontroller/gps-data-parsing.md) | [Italiano](../../it/02-51-microcontroller/gps-data-parsing.md) | [日本語](../../ja/02-51-microcontroller/gps-data-parsing.md) | [한국어](../../ko/02-51-microcontroller/gps-data-parsing.md) | [Português (BR)](../../pt-br/02-51-microcontroller/gps-data-parsing.md) | Português (PT) | [简体中文](../../zh-hans/02-51-microcontroller/gps-data-parsing.md) | [繁體中文](../../zh-hant/02-51-microcontroller/gps-data-parsing.md)

**Análise de Dados GPS**

**1. Objetivos**

Nesta lição utilizamos um microcontrolador STC89C52RC (8051) juntamente com o módulo GPS para analisar a informação de posição.

**2. Preparação**

O módulo GPS comunica por UART e USB. Aqui lemos os dados através da UART do 8051: ligue o TX do módulo ao pino P3.0 da placa 8051, e o VCC e o GND a 5 V e GND.

![ligações](../../en/02-51-microcontroller/images/1.png)

**3. Programa**

Inicialize a porta série e o array de dados.

![código](../../en/02-51-microcontroller/images/2.jpg)

Leia e analise os dados recebidos.

![código](../../en/02-51-microcontroller/images/3.jpg)

Imprima os dados recebidos através da porta série.

![código](../../en/02-51-microcontroller/images/4.jpg)

**4. Resultado**

Após a alimentação, o módulo precisa de cerca de 32 s para arrancar; a partir daí, o LED de estado da porta série pisca de forma contínua e os dados podem ser recebidos normalmente.

Descarregue e execute o programa, abra um terminal série a 9600 baud, e a informação de posição atual é impressa em ciclo.

![saída série](../../en/02-51-microcontroller/images/5.jpg)

Tenha em conta que a antena do módulo tem de estar ao ar livre, caso contrário pode não adquirir sinal GPS.
