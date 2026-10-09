[English](../../en/07-jetson-nano-agnss/baidu-map-api-key.md) | [Deutsch](../../de/07-jetson-nano-agnss/baidu-map-api-key.md) | [Español](../../es/07-jetson-nano-agnss/baidu-map-api-key.md) | [Français](../../fr/07-jetson-nano-agnss/baidu-map-api-key.md) | [Italiano](../../it/07-jetson-nano-agnss/baidu-map-api-key.md) | [日本語](../../ja/07-jetson-nano-agnss/baidu-map-api-key.md) | [한국어](../../ko/07-jetson-nano-agnss/baidu-map-api-key.md) | [Português (BR)](../../pt-br/07-jetson-nano-agnss/baidu-map-api-key.md) | Português (PT) | [简体中文](../../zh-hans/07-jetson-nano-agnss/baidu-map-api-key.md) | [繁體中文](../../zh-hant/07-jetson-nano-agnss/baidu-map-api-key.md)

**Como obter uma chave de API do Baidu Maps**

**1. Registo**

Aceda à plataforma aberta do Baidu Maps: <https://lbsyun.baidu.com/>

Desça até ao fim da página e clique em "Register now".

![registo](../../en/07-jetson-nano-agnss/images/18.jpg)

Recomenda-se o registo como programador individual, uma vez que a chave pode ser utilizada no próprio dia.

Siga as instruções para concluir o registo.

![passos do registo](../../en/07-jetson-nano-agnss/images/19.jpg)

**2. Obter a AK**

O serviço utilizado aqui é o serviço de localização por IP da Web Service API. A respetiva documentação está em:

<https://lbsyun.baidu.com/index.php?title=webapi/ip-api>

Clique em **Console**, escolha **My Applications** e depois **Create Application**.

![consola](../../en/07-jetson-nano-agnss/images/20.jpg)

Dê à aplicação qualquer nome, escolha **Server side** como tipo de aplicação, ative o serviço e introduza `0.0.0.0/0` na lista de permissões.

![criar aplicação](../../en/07-jetson-nano-agnss/images/21.jpg)

Clique em **Submit** para criar a aplicação.

![submetido](../../en/07-jetson-nano-agnss/images/22.jpg)

Copie o valor da AK da aplicação.

![copiar ak](../../en/07-jetson-nano-agnss/images/23.jpg)

Cole-o no programa e guarde — a partir daí pode ler a informação de posição através do Baidu Maps.

![colar ak](../../en/07-jetson-nano-agnss/images/24.jpg)
