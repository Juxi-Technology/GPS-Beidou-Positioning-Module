[English](../../en/06-jetson-nano-position-parse/position-parse.md) | [Deutsch](../../de/06-jetson-nano-position-parse/position-parse.md) | [Español](../../es/06-jetson-nano-position-parse/position-parse.md) | [Français](../../fr/06-jetson-nano-position-parse/position-parse.md) | [Italiano](../../it/06-jetson-nano-position-parse/position-parse.md) | [日本語](../../ja/06-jetson-nano-position-parse/position-parse.md) | [한국어](../../ko/06-jetson-nano-position-parse/position-parse.md) | Português (BR) | [Português (PT)](../../pt-pt/06-jetson-nano-position-parse/position-parse.md) | [简体中文](../../zh-hans/06-jetson-nano-position-parse/position-parse.md) | [繁體中文](../../zh-hant/06-jetson-nano-position-parse/position-parse.md)

**Leitura e análise dos dados de posição do GPS (Jetson)**

**1. Objetivos**

Nesta lição usamos um Jetson Orin e o módulo GPS para ler e analisar as informações de posição.

**2. Preparação**

O módulo GPS suporta comunicação UART ou USB; aqui usamos USB.

![módulo](../../en/06-jetson-nano-position-parse/images/1.png)

Conecte o Jetson Orin ao módulo GPS com um cabo Type-C e execute `ls /dev | grep 'ttyUSB'` — o módulo é detectado como `USB0`.

![detecção do dispositivo](../../en/06-jetson-nano-position-parse/images/2.jpg)

**3. Programa**

O programa desta lição é `GPS.py`.

Inicialize o USB:

![código](../../en/06-jetson-nano-position-parse/images/3.jpg)

A função de aquisição e análise de posição filtra os dados recebidos em busca de sentenças que começam com `GNGGA` e as analisa em variáveis globais.

![código](../../en/06-jetson-nano-position-parse/images/4.jpg)

![código](../../en/06-jetson-nano-position-parse/images/5.jpg)

A mesma abordagem lê e analisa as informações de rumo a partir de `GNVTG`.

![código](../../en/06-jetson-nano-position-parse/images/6.jpg)

Os dados analisados são impressos em loop.

![código](../../en/06-jetson-nano-position-parse/images/7.jpg)

**4. Executando o programa**

Execute `sudo python3 GPS.py` em um terminal.

**5. Resultado**

Após a energização, o módulo leva cerca de 32 s para iniciar; depois disso, o LED de status da serial pisca continuamente e os dados podem ser recebidos normalmente.

Quando o programa inicia, ele inicializa o USB e imprime `GPS Serial Opened! Baudrate=9600` em caso de sucesso, ou `GPS Serial Open Failed!` em caso de falha — se falhar, verifique a ligação ou a porta USB. Em seguida, imprime as informações de posição e rumo em loop.

![saída](../../en/06-jetson-nano-position-parse/images/8.jpg)

Pressione Ctrl+C para parar a leitura.

![saída](../../en/06-jetson-nano-position-parse/images/9.jpg)

Observe que a antena do módulo precisa estar ao ar livre, caso contrário pode não adquirir o sinal de GPS — quando nenhum sinal é encontrado, ele imprime `GPS no found`.
