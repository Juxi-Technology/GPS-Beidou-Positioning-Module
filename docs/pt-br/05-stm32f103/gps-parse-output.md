[English](../../en/05-stm32f103/gps-parse-output.md) | [Deutsch](../../de/05-stm32f103/gps-parse-output.md) | [Español](../../es/05-stm32f103/gps-parse-output.md) | [Français](../../fr/05-stm32f103/gps-parse-output.md) | [Italiano](../../it/05-stm32f103/gps-parse-output.md) | [日本語](../../ja/05-stm32f103/gps-parse-output.md) | [한국어](../../ko/05-stm32f103/gps-parse-output.md) | Português (BR) | [Português (PT)](../../pt-pt/05-stm32f103/gps-parse-output.md) | [简体中文](../../zh-hans/05-stm32f103/gps-parse-output.md) | [繁體中文](../../zh-hant/05-stm32f103/gps-parse-output.md)

**Análise e saída dos dados do GPS (STM32)**

**1. Objetivos**

Nesta lição usamos um STM32F103C8T6 e o módulo GPS para analisar e enviar as informações de posição.

**2. Preparação**

O módulo GPS se comunica por UART e USB. Aqui usamos a UART do STM32: conecte o TXD do módulo ao pino PA10 da placa STM32F103C8T6, e o VCC e o GND aos 5 V e ao GND da placa. Conecte o GND e o RXD do adaptador TTL ao GND e ao PA9 do STM32.

![ligação](../../en/05-stm32f103/images/1.png)

**3. Programa**

O baud rate do módulo é 9600.

![código](../../en/05-stm32f103/images/2.jpg)

Leia e analise os dados recebidos.

![código](../../en/05-stm32f103/images/3.jpg)

Converta as unidades de latitude / longitude para graus.

![código](../../en/05-stm32f103/images/4.jpg)

Imprima os dados recebidos pela porta serial.

![código](../../en/05-stm32f103/images/5.jpg)

Observação: a latitude e a longitude do GPS / BeiDou não têm uma relação simples de ×100 — elas precisam de uma conversão de graus-minutos. Por exemplo, para a latitude `2429.53531` N e a longitude `11810.78036` E:

```
24 + (29.53531 / 60) ≈ 24.49225517
118 + (10.78036 / 60) ≈ 118.17967267
```

Microcontroladores diferentes também podem introduzir um pequeno erro por causa da precisão da conversão de dados.

**4. Resultado**

Após a energização, o módulo leva cerca de 32 s para iniciar; depois disso, o LED de status da serial pisca continuamente e os dados podem ser recebidos normalmente.

Baixe e execute o programa, abra um terminal serial a 9600 baud e as informações de posição atuais são impressas em loop.

![saída serial](../../en/05-stm32f103/images/6.jpg)

Observe que a antena do módulo precisa estar ao ar livre, caso contrário pode não adquirir o sinal de GPS.
