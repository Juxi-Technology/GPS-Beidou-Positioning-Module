[English](../../en/09-raspberry-pi-agnss/agnss.md) | [Deutsch](../../de/09-raspberry-pi-agnss/agnss.md) | [Español](../../es/09-raspberry-pi-agnss/agnss.md) | [Français](../../fr/09-raspberry-pi-agnss/agnss.md) | [Italiano](../../it/09-raspberry-pi-agnss/agnss.md) | [日本語](../../ja/09-raspberry-pi-agnss/agnss.md) | [한국어](../../ko/09-raspberry-pi-agnss/agnss.md) | [Português (BR)](../../pt-br/09-raspberry-pi-agnss/agnss.md) | Português (PT) | [简体中文](../../zh-hans/09-raspberry-pi-agnss/agnss.md) | [繁體中文](../../zh-hant/09-raspberry-pi-agnss/agnss.md)

**Posicionamento Assistido por AGNSS**

**1. Objetivos**

Nesta lição utilizamos uma Raspberry Pi, o módulo GPS e um servidor AGNSS para ler e analisar a informação de posição em condições de sinal fraco.

**2. Sobre o AGNSS**

2.1 **Porquê usar AGNSS**

- Um recetor GNSS autónomo tem de adquirir e seguir os sinais dos satélites e descodificar a mensagem de navegação antes de conseguir fixar a sua posição.
- Num ambiente de sinal forte, consegue arrancar a frio em cerca de 30 segundos. Num ambiente de sinal fraco, a aquisição é lenta e a mensagem de navegação é difícil de descodificar, pelo que um fix pode demorar muito tempo ou nunca acontecer.
- O AGNSS fornece ao recetor a assistência de que este precisa — dados de navegação, uma posição aproximada e a hora. Tanto em condições de sinal forte como fraco, isto encurta significativamente o tempo até ao primeiro fix (TTFF).

2.2 **Como funciona**

- Um servidor AGNSS recolhe e gere os dados de assistência de várias fontes GNSS e responde aos pedidos dos clientes (que exigem um nome de utilizador e uma palavra-passe).
- O cliente obtém os dados de assistência através de TCP/IP e reencaminha-os para o recetor GNSS.
- Também pode executar o seu próprio servidor proxy.

![arquitetura](../../en/09-raspberry-pi-agnss/images/1.png)

2.3 **Procedimento**

- Ligar ao servidor AGNSS
  - Endereço: `121.41.40.95` (domínio `www.gnss-aide.com`)
  - Porta: `2621`
- Enviar um pedido AGNSS
  - String de pedido (o nome de utilizador e a palavra-passe são obrigatórios):
  - `user=<your-username>;pwd=<your-password>;cmd=full;gnss=gps+bd;lat=60.0;lon=55.0;alt=0;`
- Receber os dados de assistência
- Reencaminhá-los para o recetor

2.4 **Parâmetros do pedido**

O pedido é uma sequência de pares `chave=valor;`, por exemplo `chave=valor;chave=valor;`.

Exemplo: `user=<your-username>;pwd=<your-password>;cmd=full;gnss=gps+bd;lat=60.0;lon=55.0;alt=0;`

| Chave | Valor | Obrigatório | Observações |
| --- | --- | --- | --- |
| **user** | string | sim | Nome de utilizador. Recomenda-se vivamente usar um endereço de e-mail válido — os avisos importantes de manutenção do servidor AGNSS são enviados para lá. |
| **pwd** | string | sim | Palavra-passe do utilizador |
| **gnss** | string | não | Lista de GNSS separada por vírgulas; atualmente o GPS é suportado. Os valores válidos são `gps`, `bds`, `glo`. `gnss=gps;` pede assistência de GPS, `gnss=gps,bds;` pede assistência de GPS e BDS. |
| **cmd** | string | não | `full`: toda a informação, incluindo efemérides, hora estimada e posição. `eph`: apenas efemérides. `aid`: hora e posição de assistência. O valor predefinido é `full`. |
| **lat** | número | não | Latitude estimada do utilizador, em graus (-90 a 90). A assistência de posição vem em dois formatos — lat/lon/alt ou ECEF — e escolhe-se um. O formato lat/lon/alt exige os três campos: `lat=30;lon=120.3;alt=100;` |
| **lon** | número | não | Longitude estimada do utilizador, em graus (-180 a 180). |
| **alt** | número | não | Altitude estimada do utilizador, em metros. |
| **x** | número | não | ECEF X estimado do utilizador, em metros. O formato ECEF exige os três campos: `x=30000;y=1111120.3;z=3345100;` |
| **y** | número | não | ECEF Y estimado do utilizador, em metros. |
| **z** | número | não | ECEF Z estimado do utilizador, em metros. |
| **pacc** | número | não | Precisão da posição do utilizador, em metros. |

2.5 **Resposta do servidor**

![resposta](../../en/09-raspberry-pi-agnss/images/2.png)

- O servidor devolve um cabeçalho de dados seguido dos dados de assistência.
- A carga útil binária são os dados de assistência de que o recetor precisa e traz o seu próprio checksum. Para o formato binário, consulte a especificação do protocolo do recetor CASIC.
- Reencaminhar também o cabeçalho para o recetor é inofensivo.

2.6 **Desempenho**

Em comparação com um recetor GNSS autónomo, um recetor AGNSS melhora significativamente o TTFF, especialmente em condições de sinal fraco.

![comparação de TTFF](../../en/09-raspberry-pi-agnss/images/3.jpg)

2.7 **Observações**

- A posição aproximada tem de ser obtida de outra forma, por exemplo a partir de:
  - um módulo GSM/GPRS/3G, que pode derivar uma posição aproximada a partir do ID da célula
  - Wi-Fi ou outro módulo sem fios, que também pode localizar de forma aproximada
- A posição aproximada tem de ter uma precisão de 15 km; uma indicação de posição incorreta degrada o desempenho do recetor.
- Se não estiver disponível nenhuma posição aproximada, omita os campos de posição (lat, lon, alt, x, y, z) do pedido — o recetor recorre então ao seu último fix válido.
- Não é necessário usar a própria saída do recetor como posição aproximada.

2.8 **Quando o AGNSS é necessário**

Não é necessário descarregar do servidor em cada arranque, o que poupa largura de banda:

- Os chips CASIC têm uma SRAM com bateria de apoio e uma flash de backup permanente que retêm os dados de efemérides recebidos.
- Durante o funcionamento normal, o chip continua a descarregar as efemérides mais recentes dos satélites.
- Pode consultar o estado do recetor para decidir se é necessário descarregar. O recetor pode emitir uma frase de estado da mensagem de navegação (desativada por predefinição; tem de ser configurada).

2.9 **A frase de estado da mensagem de navegação**

![frase 1](../../en/09-raspberry-pi-agnss/images/4.png)

![frase 2](../../en/09-raspberry-pi-agnss/images/5.png)

- Esta frase indica a hora interna do recetor e o estado da mensagem de navegação.
- Envie `$PCAS03,,,,,,,,,,,1*1F` para a emitir uma vez por segundo.
- Envie `$PCAS03,,,,,,,,,,,0*1E` para deixar de a emitir.
- Nota: cada frase tem de terminar com `\r\n` (0x0D, 0x0A) e contém 11 vírgulas.
- Se o indicador de hora for válido (diferente de zero) e o número de efemérides válidas for elevado (mais de 8), não é necessário descarregar as efemérides do AGNSS.

**3. Preparação**

**3.1 Ligações**

O módulo GPS suporta comunicação por UART ou USB; aqui utilizamos USB.

![ligações](../../en/09-raspberry-pi-agnss/images/6.png)

Ligue a Raspberry Pi ao módulo GPS com um cabo Type-C e, em seguida, execute `ls /dev | grep 'ttyUSB'` — o módulo é detetado como `USB0`.

![deteção do dispositivo](../../en/09-raspberry-pi-agnss/images/7.png)

**3.2 Obter uma AK do Baidu Maps**

Consulte [Como obter uma chave de API do Baidu Maps](baidu-map-api-key.md).

**4. Programa**

O programa desta lição é `GPS-agnss.py`.

Inicialize o USB:

![código](../../en/09-raspberry-pi-agnss/images/8.jpg)

Preencha a AK que obteve, e a latitude e a longitude aproximadas atuais podem então ser lidas no Baidu Maps.

![código](../../en/09-raspberry-pi-agnss/images/9.jpg)

As coordenadas aproximadas do Baidu Maps são enviadas ao servidor — use a sua própria conta AGNSS — e, quando tudo estiver pronto, o pacote completo é enviado ao módulo.

![código](../../en/09-raspberry-pi-agnss/images/10.jpg)

![código](../../en/09-raspberry-pi-agnss/images/11.jpg)

A função de aquisição e análise de posição filtra os dados recebidos à procura de frases que começam por `GNGGA` e analisa-as para variáveis globais.

![código](../../en/09-raspberry-pi-agnss/images/12.jpg)

![código](../../en/09-raspberry-pi-agnss/images/13.jpg)

A mesma abordagem lê e analisa a informação de rumo a partir de `GNVTG`.

![código](../../en/09-raspberry-pi-agnss/images/14.jpg)

Os dados analisados são impressos em ciclo.

![código](../../en/09-raspberry-pi-agnss/images/15.jpg)

**5. Executar o programa**

Execute `sudo python2 GPS-agnss.py` num terminal.

**6. Resultado**

**Nota: com o posicionamento assistido, a Raspberry Pi tem de ter acesso à rede.**

Após a alimentação, num ambiente de sinal fraco, o programa inicializa o USB e imprime `GPS Serial Opened! Baudrate=9600` em caso de sucesso, ou `GPS Serial Open Failed!` em caso de falha — se falhar, verifique as ligações ou a porta USB.

Em seguida, imprime `GPS Agnss start` enquanto envia os dados de assistência ao servidor, e `GPS Agnss success` quando termina.

Enquanto não adquire um sinal GPS, imprime `GPS no found` juntamente com as coordenadas aproximadas lidas no Baidu Maps.

![saída](../../en/09-raspberry-pi-agnss/images/16.jpg)

Assim que o sinal é adquirido, imprime a informação de posição e de rumo em ciclo.

![saída](../../en/09-raspberry-pi-agnss/images/17.jpg)

Prima Ctrl+C para parar a leitura.

![saída](../../en/09-raspberry-pi-agnss/images/18.jpg)
