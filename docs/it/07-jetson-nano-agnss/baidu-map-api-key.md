[English](../../en/07-jetson-nano-agnss/baidu-map-api-key.md) | [Deutsch](../../de/07-jetson-nano-agnss/baidu-map-api-key.md) | [Español](../../es/07-jetson-nano-agnss/baidu-map-api-key.md) | [Français](../../fr/07-jetson-nano-agnss/baidu-map-api-key.md) | Italiano | [日本語](../../ja/07-jetson-nano-agnss/baidu-map-api-key.md) | [한국어](../../ko/07-jetson-nano-agnss/baidu-map-api-key.md) | [Português (BR)](../../pt-br/07-jetson-nano-agnss/baidu-map-api-key.md) | [Português (PT)](../../pt-pt/07-jetson-nano-agnss/baidu-map-api-key.md) | [简体中文](../../zh-hans/07-jetson-nano-agnss/baidu-map-api-key.md) | [繁體中文](../../zh-hant/07-jetson-nano-agnss/baidu-map-api-key.md)

**Richiesta di una chiave API di Baidu Maps**

**1. Registrazione**

Andare alla piattaforma aperta di Baidu Maps: <https://lbsyun.baidu.com/>

Scorrere fino in fondo alla pagina e fare clic su "Register now".

![registrazione](../../en/07-jetson-nano-agnss/images/18.jpg)

Si consiglia la registrazione come sviluppatore individuale, poiché la chiave può essere utilizzata lo stesso giorno.

Seguire le istruzioni per completare la registrazione.

![passaggi di registrazione](../../en/07-jetson-nano-agnss/images/19.jpg)

**2. Ottenere l'AK**

Il servizio utilizzato qui è il servizio di localizzazione IP dell'API Web Service. La sua documentazione è disponibile all'indirizzo:

<https://lbsyun.baidu.com/index.php?title=webapi/ip-api>

Fare clic su **Console**, scegliere **My Applications**, quindi **Create Application**.

![console](../../en/07-jetson-nano-agnss/images/20.jpg)

Dare all'applicazione un nome qualsiasi, scegliere **Server side** come tipo di applicazione, abilitare il servizio e inserire `0.0.0.0/0` nella whitelist.

![creazione dell'applicazione](../../en/07-jetson-nano-agnss/images/21.jpg)

Fare clic su **Submit** per creare l'applicazione.

![inviata](../../en/07-jetson-nano-agnss/images/22.jpg)

Copiare il valore AK dell'applicazione.

![copia AK](../../en/07-jetson-nano-agnss/images/23.jpg)

Incollarlo nel programma e salvare — si potranno quindi leggere le informazioni di posizione tramite Baidu Maps.

![incolla AK](../../en/07-jetson-nano-agnss/images/24.jpg)
