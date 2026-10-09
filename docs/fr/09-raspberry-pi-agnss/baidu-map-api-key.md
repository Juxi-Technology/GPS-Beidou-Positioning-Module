[English](../../en/09-raspberry-pi-agnss/baidu-map-api-key.md) | [Deutsch](../../de/09-raspberry-pi-agnss/baidu-map-api-key.md) | [Español](../../es/09-raspberry-pi-agnss/baidu-map-api-key.md) | Français | [Italiano](../../it/09-raspberry-pi-agnss/baidu-map-api-key.md) | [日本語](../../ja/09-raspberry-pi-agnss/baidu-map-api-key.md) | [한국어](../../ko/09-raspberry-pi-agnss/baidu-map-api-key.md) | [Português (BR)](../../pt-br/09-raspberry-pi-agnss/baidu-map-api-key.md) | [Português (PT)](../../pt-pt/09-raspberry-pi-agnss/baidu-map-api-key.md) | [简体中文](../../zh-hans/09-raspberry-pi-agnss/baidu-map-api-key.md) | [繁體中文](../../zh-hant/09-raspberry-pi-agnss/baidu-map-api-key.md)

**Demander une clé d'API Baidu Maps**

**1. Inscription**

Rendez-vous sur la plateforme ouverte Baidu Maps : <https://lbsyun.baidu.com/>

Faites défiler la page jusqu'en bas et cliquez sur « Register now ».

![inscription](../../en/09-raspberry-pi-agnss/images/19.jpg)

Il est recommandé de s'inscrire en tant que développeur individuel, car la clé peut alors être utilisée le jour même.

Suivez les instructions pour terminer l'inscription.

![étapes d'inscription](../../en/09-raspberry-pi-agnss/images/20.jpg)

**2. Obtenir l'AK**

Le service utilisé ici est le service de localisation par IP de la Web Service API. Sa documentation se trouve à l'adresse :

<https://lbsyun.baidu.com/index.php?title=webapi/ip-api>

Cliquez sur **Console**, choisissez **My Applications**, puis **Create Application**.

![console](../../en/09-raspberry-pi-agnss/images/21.jpg)

Donnez n'importe quel nom à l'application, choisissez **Server side** comme type d'application, activez le service et saisissez `0.0.0.0/0` dans la liste blanche.

![créer une application](../../en/09-raspberry-pi-agnss/images/22.jpg)

Cliquez sur **Submit** pour créer l'application.

![soumise](../../en/09-raspberry-pi-agnss/images/23.jpg)

Copiez la valeur AK de l'application.

![copier l'AK](../../en/09-raspberry-pi-agnss/images/24.jpg)

Collez-la dans le programme et enregistrez — vous pouvez alors lire les informations de position via Baidu Maps.

![coller l'AK](../../en/09-raspberry-pi-agnss/images/25.jpg)
