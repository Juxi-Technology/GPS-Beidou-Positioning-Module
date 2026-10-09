[English](../../en/04-arduino-position-parse/position-parse.md) | [Deutsch](../../de/04-arduino-position-parse/position-parse.md) | [Español](../../es/04-arduino-position-parse/position-parse.md) | [Français](../../fr/04-arduino-position-parse/position-parse.md) | [Italiano](../../it/04-arduino-position-parse/position-parse.md) | [日本語](../../ja/04-arduino-position-parse/position-parse.md) | [한국어](../../ko/04-arduino-position-parse/position-parse.md) | Português (BR) | [Português (PT)](../../pt-pt/04-arduino-position-parse/position-parse.md) | [简体中文](../../zh-hans/04-arduino-position-parse/position-parse.md) | [繁體中文](../../zh-hant/04-arduino-position-parse/position-parse.md)

**Análise dos dados de posição do GPS**

**1. Objetivos**

Nesta lição usamos um Arduino e o módulo GPS para analisar as informações de posição e imprimi-las.

**2. Preparação**

O módulo GPS se comunica por UART e USB. Aqui usamos a UART do Arduino UNO: conecte o TX do módulo ao pino D0 do UNO, e o VCC e o GND aos 5 V e ao GND.

![ligação](../../en/04-arduino-position-parse/images/1.png)

**3. Programa**

Inicialize a porta serial.

![código](../../en/04-arduino-position-parse/images/2.jpg)

Leia os dados da serial.

![código](../../en/04-arduino-position-parse/images/3.jpg)

Analise os dados da serial.

![código](../../en/04-arduino-position-parse/images/4.jpg)

Imprima as informações de posição analisadas.

![código](../../en/04-arduino-position-parse/images/5.jpg)

**4. Compilar e enviar**

4.1 Abra o arquivo na Arduino IDE, clique no botão "✓" para compilar e aguarde "Done compiling".

![compilação](../../en/04-arduino-position-parse/images/6.jpg)

4.2 No menu, selecione Ferramentas → Porta → a porta mostrada no Gerenciador de Dispositivos.

![seleção de porta](../../en/04-arduino-position-parse/images/7.jpg)

4.3 Clique no botão "→" para enviar. Quando aparecer "Done uploading", o envio foi concluído com sucesso.

![envio](../../en/04-arduino-position-parse/images/8.jpg)

**5. Resultado**

Após a energização, o módulo leva cerca de 32 s para iniciar; depois disso, o LED de status da serial pisca continuamente e os dados podem ser recebidos normalmente.

Execute o programa, abra o monitor serial a 9600 baud e as informações de posição em tempo real analisadas são impressas em loop.

![saída serial](../../en/04-arduino-position-parse/images/9.jpg)

Observe que a antena do módulo precisa estar ao ar livre, caso contrário pode não adquirir o sinal de GPS.
