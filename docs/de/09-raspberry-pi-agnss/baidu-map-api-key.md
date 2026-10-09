[English](../../en/09-raspberry-pi-agnss/baidu-map-api-key.md) | Deutsch | [Español](../../es/09-raspberry-pi-agnss/baidu-map-api-key.md) | [Français](../../fr/09-raspberry-pi-agnss/baidu-map-api-key.md) | [Italiano](../../it/09-raspberry-pi-agnss/baidu-map-api-key.md) | [日本語](../../ja/09-raspberry-pi-agnss/baidu-map-api-key.md) | [한국어](../../ko/09-raspberry-pi-agnss/baidu-map-api-key.md) | [Português (BR)](../../pt-br/09-raspberry-pi-agnss/baidu-map-api-key.md) | [Português (PT)](../../pt-pt/09-raspberry-pi-agnss/baidu-map-api-key.md) | [简体中文](../../zh-hans/09-raspberry-pi-agnss/baidu-map-api-key.md) | [繁體中文](../../zh-hant/09-raspberry-pi-agnss/baidu-map-api-key.md)

**Beantragen eines Baidu-Maps-API-Schlüssels**

**1. Registrierung**

Rufen Sie die offene Plattform von Baidu Maps auf: <https://lbsyun.baidu.com/>

Scrollen Sie zum Seitenende und klicken Sie auf "Register now".

![Registrierung](../../en/09-raspberry-pi-agnss/images/19.jpg)

Die Registrierung als Einzelentwickler wird empfohlen, da der Schlüssel noch am selben Tag verwendet werden kann.

Folgen Sie den Anweisungen, um die Registrierung abzuschließen.

![Registrierungsschritte](../../en/09-raspberry-pi-agnss/images/20.jpg)

**2. Den AK beschaffen**

Der hier verwendete Dienst ist der IP-Standortdienst aus der Web Service API. Seine Dokumentation finden Sie unter:

<https://lbsyun.baidu.com/index.php?title=webapi/ip-api>

Klicken Sie auf **Console**, wählen Sie **My Applications** und dann **Create Application**.

![Konsole](../../en/09-raspberry-pi-agnss/images/21.jpg)

Geben Sie der Anwendung einen beliebigen Namen, wählen Sie **Server side** als Anwendungstyp, aktivieren Sie den Dienst und geben Sie `0.0.0.0/0` in die Whitelist ein.

![Anwendung erstellen](../../en/09-raspberry-pi-agnss/images/22.jpg)

Klicken Sie auf **Submit**, um die Anwendung zu erstellen.

![Übermittelt](../../en/09-raspberry-pi-agnss/images/23.jpg)

Kopieren Sie den AK-Wert der Anwendung.

![AK kopieren](../../en/09-raspberry-pi-agnss/images/24.jpg)

Fügen Sie ihn in das Programm ein und speichern Sie — anschließend können Sie Positionsinformationen über Baidu Maps auslesen.

![AK einfügen](../../en/09-raspberry-pi-agnss/images/25.jpg)
