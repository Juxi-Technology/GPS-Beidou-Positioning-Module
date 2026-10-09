English | [Deutsch](../../de/09-raspberry-pi-agnss/baidu-map-api-key.md) | [Español](../../es/09-raspberry-pi-agnss/baidu-map-api-key.md) | [Français](../../fr/09-raspberry-pi-agnss/baidu-map-api-key.md) | [Italiano](../../it/09-raspberry-pi-agnss/baidu-map-api-key.md) | [日本語](../../ja/09-raspberry-pi-agnss/baidu-map-api-key.md) | [한국어](../../ko/09-raspberry-pi-agnss/baidu-map-api-key.md) | [Português (BR)](../../pt-br/09-raspberry-pi-agnss/baidu-map-api-key.md) | [Português (PT)](../../pt-pt/09-raspberry-pi-agnss/baidu-map-api-key.md) | [简体中文](../../zh-hans/09-raspberry-pi-agnss/baidu-map-api-key.md) | [繁體中文](../../zh-hant/09-raspberry-pi-agnss/baidu-map-api-key.md)

**Applying for a Baidu Map API Key**

**1. Registration**

Go to the Baidu Map open platform: <https://lbsyun.baidu.com/>

Scroll to the bottom of the page and click "Register now".

![register](images/19.jpg)

Registering as an individual developer is recommended, since the key can be used the same day.

Follow the prompts to complete registration.

![registration steps](images/20.jpg)

**2. Getting the AK**

The service used here is the IP location service from the Web Service API. Its documentation is at:

<https://lbsyun.baidu.com/index.php?title=webapi/ip-api>

Click **Console**, choose **My Applications**, then **Create Application**.

![console](images/21.jpg)

Give the application any name, choose **Server side** as the application type, enable the service, and enter `0.0.0.0/0` in the whitelist.

![create application](images/22.jpg)

Click **Submit** to create the application.

![submitted](images/23.jpg)

Copy the application's AK value.

![copy ak](images/24.jpg)

Paste it into the program and save — you can then read position information through Baidu Maps.

![paste ak](images/25.jpg)
