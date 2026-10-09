[English](../../en/04-arduino-position-parse/position-parse.md) | [Deutsch](../../de/04-arduino-position-parse/position-parse.md) | [Español](../../es/04-arduino-position-parse/position-parse.md) | [Français](../../fr/04-arduino-position-parse/position-parse.md) | [Italiano](../../it/04-arduino-position-parse/position-parse.md) | [日本語](../../ja/04-arduino-position-parse/position-parse.md) | [한국어](../../ko/04-arduino-position-parse/position-parse.md) | [Português (BR)](../../pt-br/04-arduino-position-parse/position-parse.md) | Português (PT) | [简体中文](../../zh-hans/04-arduino-position-parse/position-parse.md) | [繁體中文](../../zh-hant/04-arduino-position-parse/position-parse.md)

**Análise de Dados de Posição GPS**

**1. Objetivos**

Nesta lição utilizamos um Arduino e o módulo GPS para analisar a informação de posição e imprimi-la.

**2. Preparação**

O módulo GPS comunica por UART e USB. Aqui utilizamos a UART do Arduino UNO: ligue o TX do módulo ao pino D0 do UNO, e o VCC e o GND a 5 V e GND.

![ligações](../../en/04-arduino-position-parse/images/1.png)

**3. Programa**

Inicialize a porta série.

![código](../../en/04-arduino-position-parse/images/2.jpg)

Leia os dados da porta série.

![código](../../en/04-arduino-position-parse/images/3.jpg)

Analise os dados da porta série.

![código](../../en/04-arduino-position-parse/images/4.jpg)

Imprima a informação de posição analisada.

![código](../../en/04-arduino-position-parse/images/5.jpg)

**4. Compilar e carregar**

4.1 Abra o ficheiro no Arduino IDE, clique no botão "✓" para compilar e aguarde "Done compiling".

![compilação](../../en/04-arduino-position-parse/images/6.jpg)

4.2 No menu, selecione Ferramentas → Porta → a porta indicada no Gestor de Dispositivos.

![seleção de porta](../../en/04-arduino-position-parse/images/7.jpg)

4.3 Clique no botão "→" para carregar. Quando aparecer "Done uploading", o carregamento foi bem-sucedido.

![carregamento](../../en/04-arduino-position-parse/images/8.jpg)

**5. Resultado**

Após a alimentação, o módulo precisa de cerca de 32 s para arrancar; a partir daí, o LED de estado da porta série pisca de forma contínua e os dados podem ser recebidos normalmente.

Execute o programa, abra o monitor série a 9600 baud, e a informação de posição analisada em tempo real é impressa em ciclo.

![saída série](../../en/04-arduino-position-parse/images/9.jpg)

Tenha em conta que a antena do módulo tem de estar ao ar livre, caso contrário pode não adquirir sinal GPS.
