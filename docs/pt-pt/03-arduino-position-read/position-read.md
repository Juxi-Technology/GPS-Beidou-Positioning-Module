[English](../../en/03-arduino-position-read/position-read.md) | [Deutsch](../../de/03-arduino-position-read/position-read.md) | [Español](../../es/03-arduino-position-read/position-read.md) | [Français](../../fr/03-arduino-position-read/position-read.md) | [Italiano](../../it/03-arduino-position-read/position-read.md) | [日本語](../../ja/03-arduino-position-read/position-read.md) | [한국어](../../ko/03-arduino-position-read/position-read.md) | [Português (BR)](../../pt-br/03-arduino-position-read/position-read.md) | Português (PT) | [简体中文](../../zh-hans/03-arduino-position-read/position-read.md) | [繁體中文](../../zh-hant/03-arduino-position-read/position-read.md)

**Leitura de Dados de Posição GPS**

**1. Objetivos**

Nesta lição utilizamos um Arduino e o módulo GPS para ler a informação de posição.

**2. Preparação**

O módulo GPS comunica por UART e USB. Aqui utilizamos a UART do Arduino UNO: ligue o TX do módulo ao pino D0 do UNO, e o VCC e o GND a 5 V e GND.

![ligações](../../en/03-arduino-position-read/images/1.png)

**3. Programa**

Inicialize a porta série.

![código](../../en/03-arduino-position-read/images/2.jpg)

Imprima os dados recebidos.

**4. Compilar e carregar**

4.1 Abra o ficheiro no Arduino IDE, clique no botão "✓" da barra de ferramentas para compilar e aguarde "Done compiling" na barra de estado.

![compilação](../../en/03-arduino-position-read/images/3.jpg)

4.2 No menu do Arduino IDE, selecione Ferramentas → Porta → a porta indicada no Gestor de Dispositivos, como abaixo.

![seleção de porta](../../en/03-arduino-position-read/images/4.jpg)

4.3 Em seguida, clique no botão "→" para carregar o código na placa UNO. Quando aparecer "Done uploading", o carregamento foi bem-sucedido.

![carregamento](../../en/03-arduino-position-read/images/5.jpg)

**5. Resultado**

Após a alimentação, o módulo precisa de cerca de 32 s para arrancar; a partir daí, o LED de estado da porta série pisca de forma contínua e os dados podem ser recebidos normalmente.

Execute o programa, abra o monitor série e defina a taxa de baud para 9600. A informação de posição atual é impressa em ciclo. Estes são dados brutos, não processados — consulte a [especificação do protocolo CASIC GNSS](../../../docs/datasheets/CASIC-GNSS-protocol-spec-CN.pdf) para saber o significado de cada frase.

![saída série](../../en/03-arduino-position-read/images/6.jpg)

Tenha em conta que a antena do módulo tem de estar ao ar livre, caso contrário pode não adquirir sinal GPS.
