[English](../../en/09-raspberry-pi-agnss/agnss.md) | [Deutsch](../../de/09-raspberry-pi-agnss/agnss.md) | [Español](../../es/09-raspberry-pi-agnss/agnss.md) | [Français](../../fr/09-raspberry-pi-agnss/agnss.md) | [Italiano](../../it/09-raspberry-pi-agnss/agnss.md) | [日本語](../../ja/09-raspberry-pi-agnss/agnss.md) | [한국어](../../ko/09-raspberry-pi-agnss/agnss.md) | Português (BR) | [Português (PT)](../../pt-pt/09-raspberry-pi-agnss/agnss.md) | [简体中文](../../zh-hans/09-raspberry-pi-agnss/agnss.md) | [繁體中文](../../zh-hant/09-raspberry-pi-agnss/agnss.md)

**Posicionamento assistido por AGNSS**

**1. Objetivos**

Nesta lição usamos um Raspberry Pi, o módulo GPS e um servidor AGNSS para ler e analisar as informações de posição em condições de sinal fraco.

**2. Sobre o AGNSS**

2.1 **Por que usar AGNSS**

- Um receptor GNSS autônomo precisa adquirir e rastrear os sinais dos satélites e decodificar a mensagem de navegação antes de conseguir fixar sua posição.
- Em um ambiente de sinal forte, ele consegue fazer uma partida a frio em cerca de 30 segundos. Em um ambiente de sinal fraco, a aquisição é lenta e a mensagem de navegação é difícil de decodificar, de modo que um fix pode demorar muito ou nunca acontecer.
- O AGNSS fornece ao receptor a assistência de que ele precisa — dados de navegação, uma posição aproximada e a hora. Tanto em condições de sinal forte quanto fraco, isso encurta significativamente o tempo para o primeiro fix (TTFF).

2.2 **Como funciona**

- Um servidor AGNSS coleta e gerencia os dados de assistência de várias fontes GNSS e responde às requisições dos clientes (que exigem um nome de usuário e uma senha).
- O cliente busca os dados de assistência por TCP/IP e os encaminha ao receptor GNSS.
- Você também pode executar seu próprio servidor proxy.

![arquitetura](../../en/09-raspberry-pi-agnss/images/1.png)

2.3 **Procedimento**

- Conecte-se ao servidor AGNSS
  - Endereço: `121.41.40.95` (domínio `www.gnss-aide.com`)
  - Porta: `2621`
- Envie uma requisição AGNSS
  - String de requisição (o nome de usuário e a senha são obrigatórios):
  - `user=<your-username>;pwd=<your-password>;cmd=full;gnss=gps+bd;lat=60.0;lon=55.0;alt=0;`
- Receba os dados de assistência
- Encaminhe-os ao receptor

2.4 **Parâmetros da requisição**

A requisição é uma sequência de pares `chave=valor;`, por exemplo `chave=valor;chave=valor;`.

Exemplo: `user=<your-username>;pwd=<your-password>;cmd=full;gnss=gps+bd;lat=60.0;lon=55.0;alt=0;`

| Chave | Valor | Obrigatório | Observações |
| --- | --- | --- | --- |
| **user** | string | sim | Nome de usuário. É fortemente recomendado usar um endereço de e-mail válido — avisos importantes de manutenção do servidor AGNSS são enviados para lá. |
| **pwd** | string | sim | Senha do usuário |
| **gnss** | string | não | Lista de GNSS separada por vírgulas; atualmente o GPS é suportado. Os valores válidos são `gps`, `bds`, `glo`. `gnss=gps;` solicita assistência de GPS, `gnss=gps,bds;` solicita assistência de GPS e BDS. |
| **cmd** | string | não | `full`: todas as informações, incluindo efemérides, hora estimada e posição. `eph`: apenas efemérides. `aid`: hora e posição de assistência. O padrão é `full`. |
| **lat** | número | não | Latitude estimada do usuário, em graus (-90 a 90). A assistência de posição vem em dois formatos — lat/lon/alt ou ECEF — e você escolhe um. O formato lat/lon/alt exige os três campos: `lat=30;lon=120.3;alt=100;` |
| **lon** | número | não | Longitude estimada do usuário, em graus (-180 a 180). |
| **alt** | número | não | Altitude estimada do usuário, em metros. |
| **x** | número | não | ECEF X estimado do usuário, em metros. O formato ECEF exige os três campos: `x=30000;y=1111120.3;z=3345100;` |
| **y** | número | não | ECEF Y estimado do usuário, em metros. |
| **z** | número | não | ECEF Z estimado do usuário, em metros. |
| **pacc** | número | não | Precisão da posição do usuário, em metros. |

2.5 **Resposta do servidor**

![resposta](../../en/09-raspberry-pi-agnss/images/2.png)

- O servidor retorna um cabeçalho de dados seguido dos dados de assistência.
- A carga útil binária são os dados de assistência de que o receptor precisa e traz seu próprio checksum. Para o formato binário, consulte a especificação do protocolo do receptor CASIC.
- Encaminhar também o cabeçalho ao receptor é inofensivo.

2.6 **Desempenho**

Comparado a um receptor GNSS autônomo, um receptor AGNSS melhora o TTFF significativamente, especialmente em condições de sinal fraco.

![comparação de TTFF](../../en/09-raspberry-pi-agnss/images/3.jpg)

2.7 **Observações**

- A posição aproximada deve ser obtida de outra forma, por exemplo a partir de:
  - um módulo GSM/GPRS/3G, que pode derivar uma posição aproximada a partir do ID da célula
  - Wi-Fi ou outro módulo sem fio, que também pode localizar de forma aproximada
- A posição aproximada deve ter precisão dentro de 15 km; uma indicação de posição incorreta degrada o desempenho do receptor.
- Se nenhuma posição aproximada estiver disponível, omita os campos de posição (lat, lon, alt, x, y, z) da requisição — o receptor então recorre ao seu último fix válido.
- Não há necessidade de usar a própria saída do receptor como posição aproximada.

2.8 **Quando o AGNSS é necessário**

Não há necessidade de baixar do servidor a cada inicialização, o que economiza largura de banda:

- Os chips CASIC têm uma SRAM com bateria de apoio e uma flash de backup permanente que retêm os dados de efemérides recebidos.
- Durante a operação normal, o chip continua baixando as efemérides mais recentes dos satélites.
- Você pode consultar o status do receptor para decidir se um download é necessário. O receptor pode enviar uma sentença de status da mensagem de navegação (desativada por padrão; precisa ser configurada).

2.9 **A sentença de status da mensagem de navegação**

![sentença 1](../../en/09-raspberry-pi-agnss/images/4.png)

![sentença 2](../../en/09-raspberry-pi-agnss/images/5.png)

- Esta sentença informa a hora interna do receptor e o status da mensagem de navegação.
- Envie `$PCAS03,,,,,,,,,,,1*1F` para enviá-la uma vez por segundo.
- Envie `$PCAS03,,,,,,,,,,,0*1E` para parar de enviá-la.
- Observação: toda sentença deve terminar com `\r\n` (0x0D, 0x0A) e contém 11 vírgulas.
- Se o indicador de hora for válido (diferente de zero) e o número de efemérides válidas for grande (mais de 8), não há necessidade de baixar as efemérides do AGNSS.

**3. Preparação**

**3.1 Ligação**

O módulo GPS suporta comunicação UART ou USB; aqui usamos USB.

![ligação](../../en/09-raspberry-pi-agnss/images/6.png)

Conecte o Raspberry Pi ao módulo GPS com um cabo Type-C e execute `ls /dev | grep 'ttyUSB'` — o módulo é detectado como `USB0`.

![detecção do dispositivo](../../en/09-raspberry-pi-agnss/images/7.png)

**3.2 Obtendo uma AK do Baidu Maps**

Consulte [Como obter uma chave de API do Baidu Maps](baidu-map-api-key.md).

**4. Programa**

O programa desta lição é `GPS-agnss.py`.

Inicialize o USB:

![código](../../en/09-raspberry-pi-agnss/images/8.jpg)

Preencha a AK que você obteve, e a latitude e a longitude aproximadas atuais poderão então ser lidas no Baidu Maps.

![código](../../en/09-raspberry-pi-agnss/images/9.jpg)

As coordenadas aproximadas do Baidu Maps são enviadas ao servidor — use sua própria conta AGNSS — e, quando tudo estiver pronto, o pacote inteiro é enviado ao módulo.

![código](../../en/09-raspberry-pi-agnss/images/10.jpg)

![código](../../en/09-raspberry-pi-agnss/images/11.jpg)

A função de aquisição e análise de posição filtra os dados recebidos em busca de sentenças que começam com `GNGGA` e as analisa em variáveis globais.

![código](../../en/09-raspberry-pi-agnss/images/12.jpg)

![código](../../en/09-raspberry-pi-agnss/images/13.jpg)

A mesma abordagem lê e analisa as informações de rumo a partir de `GNVTG`.

![código](../../en/09-raspberry-pi-agnss/images/14.jpg)

Os dados analisados são impressos em loop.

![código](../../en/09-raspberry-pi-agnss/images/15.jpg)

**5. Executando o programa**

Execute `sudo python2 GPS-agnss.py` em um terminal.

**6. Resultado**

**Observação: com o posicionamento assistido, o Raspberry Pi precisa ter acesso à rede.**

Após a energização em um ambiente de sinal fraco, o programa inicializa o USB e imprime `GPS Serial Opened! Baudrate=9600` em caso de sucesso, ou `GPS Serial Open Failed!` em caso de falha — se falhar, verifique a ligação ou a porta USB.

Em seguida, imprime `GPS Agnss start` enquanto envia os dados de assistência ao servidor e `GPS Agnss success` quando termina.

Até adquirir um sinal de GPS, ele imprime `GPS no found` junto com as coordenadas aproximadas lidas no Baidu Maps.

![saída](../../en/09-raspberry-pi-agnss/images/16.jpg)

Assim que o sinal é adquirido, ele imprime as informações de posição e rumo em loop.

![saída](../../en/09-raspberry-pi-agnss/images/17.jpg)

Pressione Ctrl+C para parar a leitura.

![saída](../../en/09-raspberry-pi-agnss/images/18.jpg)
