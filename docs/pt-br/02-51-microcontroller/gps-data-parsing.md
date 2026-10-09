[English](../../en/02-51-microcontroller/gps-data-parsing.md) | [Deutsch](../../de/02-51-microcontroller/gps-data-parsing.md) | [Español](../../es/02-51-microcontroller/gps-data-parsing.md) | [Français](../../fr/02-51-microcontroller/gps-data-parsing.md) | [Italiano](../../it/02-51-microcontroller/gps-data-parsing.md) | [日本語](../../ja/02-51-microcontroller/gps-data-parsing.md) | [한국어](../../ko/02-51-microcontroller/gps-data-parsing.md) | Português (BR) | [Português (PT)](../../pt-pt/02-51-microcontroller/gps-data-parsing.md) | [简体中文](../../zh-hans/02-51-microcontroller/gps-data-parsing.md) | [繁體中文](../../zh-hant/02-51-microcontroller/gps-data-parsing.md)

**Análise dos dados do GPS**

**1. Objetivos**

Nesta lição usamos um microcontrolador STC89C52RC (8051) junto com o módulo GPS para analisar as informações de posição.

**2. Preparação**

O módulo GPS se comunica por UART e USB. Aqui o lemos pela UART do 8051: conecte o TX do módulo ao pino P3.0 da placa 8051, e o VCC e o GND aos 5 V e ao GND.

![ligação](../../en/02-51-microcontroller/images/1.png)

**3. Programa**

Inicialize a porta serial e o array de dados.

![código](../../en/02-51-microcontroller/images/2.jpg)

Leia e analise os dados recebidos.

![código](../../en/02-51-microcontroller/images/3.jpg)

Imprima os dados recebidos pela porta serial.

![código](../../en/02-51-microcontroller/images/4.jpg)

**4. Resultado**

Após a energização, o módulo leva cerca de 32 s para iniciar; depois disso, o LED de status da serial pisca continuamente e os dados podem ser recebidos normalmente.

Baixe e execute o programa, abra um terminal serial a 9600 baud e as informações de posição atuais são impressas em loop.

![saída serial](../../en/02-51-microcontroller/images/5.jpg)

Observe que a antena do módulo precisa estar ao ar livre, caso contrário pode não adquirir o sinal de GPS.
