[English](../../en/09-raspberry-pi-agnss/baidu-map-api-key.md) | [Deutsch](../../de/09-raspberry-pi-agnss/baidu-map-api-key.md) | [Español](../../es/09-raspberry-pi-agnss/baidu-map-api-key.md) | [Français](../../fr/09-raspberry-pi-agnss/baidu-map-api-key.md) | [Italiano](../../it/09-raspberry-pi-agnss/baidu-map-api-key.md) | [日本語](../../ja/09-raspberry-pi-agnss/baidu-map-api-key.md) | [한국어](../../ko/09-raspberry-pi-agnss/baidu-map-api-key.md) | Português (BR) | [Português (PT)](../../pt-pt/09-raspberry-pi-agnss/baidu-map-api-key.md) | [简体中文](../../zh-hans/09-raspberry-pi-agnss/baidu-map-api-key.md) | [繁體中文](../../zh-hant/09-raspberry-pi-agnss/baidu-map-api-key.md)

**Como obter uma chave de API do Baidu Maps**

**1. Cadastro**

Acesse a plataforma aberta do Baidu Maps: <https://lbsyun.baidu.com/>

Role até o fim da página e clique em "Register now".

![cadastro](../../en/09-raspberry-pi-agnss/images/19.jpg)

Recomenda-se cadastrar-se como desenvolvedor individual, pois a chave pode ser usada no mesmo dia.

Siga as instruções para concluir o cadastro.

![etapas do cadastro](../../en/09-raspberry-pi-agnss/images/20.jpg)

**2. Obtendo a AK**

O serviço usado aqui é o serviço de localização por IP da Web Service API. A documentação dele está em:

<https://lbsyun.baidu.com/index.php?title=webapi/ip-api>

Clique em **Console**, escolha **My Applications** e depois **Create Application**.

![console](../../en/09-raspberry-pi-agnss/images/21.jpg)

Dê ao aplicativo qualquer nome, escolha **Server side** como tipo de aplicativo, habilite o serviço e insira `0.0.0.0/0` na lista de permissões.

![criar aplicativo](../../en/09-raspberry-pi-agnss/images/22.jpg)

Clique em **Submit** para criar o aplicativo.

![enviado](../../en/09-raspberry-pi-agnss/images/23.jpg)

Copie o valor da AK do aplicativo.

![copiar ak](../../en/09-raspberry-pi-agnss/images/24.jpg)

Cole-o no programa e salve — a partir daí você pode ler as informações de posição pelo Baidu Maps.

![colar ak](../../en/09-raspberry-pi-agnss/images/25.jpg)
