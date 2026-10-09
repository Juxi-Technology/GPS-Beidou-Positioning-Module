[English](../../en/07-jetson-nano-agnss/baidu-map-api-key.md) | [Deutsch](../../de/07-jetson-nano-agnss/baidu-map-api-key.md) | [Español](../../es/07-jetson-nano-agnss/baidu-map-api-key.md) | Français | [Italiano](../../it/07-jetson-nano-agnss/baidu-map-api-key.md) | [日本語](../../ja/07-jetson-nano-agnss/baidu-map-api-key.md) | [한국어](../../ko/07-jetson-nano-agnss/baidu-map-api-key.md) | [Português (BR)](../../pt-br/07-jetson-nano-agnss/baidu-map-api-key.md) | [Português (PT)](../../pt-pt/07-jetson-nano-agnss/baidu-map-api-key.md) | [简体中文](../../zh-hans/07-jetson-nano-agnss/baidu-map-api-key.md) | [繁體中文](../../zh-hant/07-jetson-nano-agnss/baidu-map-api-key.md)

**Demander une clé d'API Baidu Maps**

**1. Inscription**

Rendez-vous sur la plateforme ouverte Baidu Maps : <https://lbsyun.baidu.com/>

Faites défiler la page jusqu'en bas et cliquez sur « Register now ».

![inscription](../../en/07-jetson-nano-agnss/images/18.jpg)

Il est recommandé de s'inscrire en tant que développeur individuel, car la clé peut alors être utilisée le jour même.

Suivez les instructions pour terminer l'inscription.

![étapes d'inscription](../../en/07-jetson-nano-agnss/images/19.jpg)

**2. Obtenir l'AK**

Le service utilisé ici est le service de localisation par IP de la Web Service API. Sa documentation se trouve à l'adresse :

<https://lbsyun.baidu.com/index.php?title=webapi/ip-api>

Cliquez sur **Console**, choisissez **My Applications**, puis **Create Application**.

![console](../../en/07-jetson-nano-agnss/images/20.jpg)

Donnez n'importe quel nom à l'application, choisissez **Server side** comme type d'application, activez le service et saisissez `0.0.0.0/0` dans la liste blanche.

![créer une application](../../en/07-jetson-nano-agnss/images/21.jpg)

Cliquez sur **Submit** pour créer l'application.

![soumise](../../en/07-jetson-nano-agnss/images/22.jpg)

Copiez la valeur AK de l'application.

![copier l'AK](../../en/07-jetson-nano-agnss/images/23.jpg)

Collez-la dans le programme et enregistrez — vous pouvez alors lire les informations de position via Baidu Maps.

![coller l'AK](../../en/07-jetson-nano-agnss/images/24.jpg)
