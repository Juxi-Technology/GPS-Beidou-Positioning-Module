[English](../../en/05-stm32f103/gps-parse-output.md) | [Deutsch](../../de/05-stm32f103/gps-parse-output.md) | [Español](../../es/05-stm32f103/gps-parse-output.md) | [Français](../../fr/05-stm32f103/gps-parse-output.md) | [Italiano](../../it/05-stm32f103/gps-parse-output.md) | [日本語](../../ja/05-stm32f103/gps-parse-output.md) | [한국어](../../ko/05-stm32f103/gps-parse-output.md) | [Português (BR)](../../pt-br/05-stm32f103/gps-parse-output.md) | Português (PT) | [简体中文](../../zh-hans/05-stm32f103/gps-parse-output.md) | [繁體中文](../../zh-hant/05-stm32f103/gps-parse-output.md)

**Análise e Saída de Dados GPS (STM32)**

**1. Objetivos**

Nesta lição utilizamos um STM32F103C8T6 e o módulo GPS para analisar e emitir a informação de posição.

**2. Preparação**

O módulo GPS comunica por UART e USB. Aqui utilizamos a UART do STM32: ligue o TXD do módulo ao pino PA10 da placa STM32F103C8T6, e o VCC e o GND aos 5 V e ao GND da placa. Ligue o GND e o RXD do adaptador TTL ao GND e ao PA9 do STM32.

![ligações](../../en/05-stm32f103/images/1.png)

**3. Programa**

A taxa de baud do módulo é 9600.

![código](../../en/05-stm32f103/images/2.jpg)

Leia e analise os dados recebidos.

![código](../../en/05-stm32f103/images/3.jpg)

Converta as unidades de latitude / longitude para graus.

![código](../../en/05-stm32f103/images/4.jpg)

Imprima os dados recebidos através da porta série.

![código](../../en/05-stm32f103/images/5.jpg)

Nota: a latitude e a longitude do GPS / BeiDou não têm uma simples relação ×100 — precisam de uma conversão de graus-minutos. Por exemplo, para a latitude `2429.53531` N e a longitude `11810.78036` E:

```
24 + (29.53531 / 60) ≈ 24.49225517
118 + (10.78036 / 60) ≈ 118.17967267
```

Diferentes microcontroladores podem também introduzir um pequeno erro devido à precisão da conversão de dados.

**4. Resultado**

Após a alimentação, o módulo precisa de cerca de 32 s para arrancar; a partir daí, o LED de estado da porta série pisca de forma contínua e os dados podem ser recebidos normalmente.

Descarregue e execute o programa, abra um terminal série a 9600 baud, e a informação de posição atual é impressa em ciclo.

![saída série](../../en/05-stm32f103/images/6.jpg)

Tenha em conta que a antena do módulo tem de estar ao ar livre, caso contrário pode não adquirir sinal GPS.
