[English](../../en/07-jetson-nano-agnss/baidu-map-api-key.md) | [Deutsch](../../de/07-jetson-nano-agnss/baidu-map-api-key.md) | Español | [Français](../../fr/07-jetson-nano-agnss/baidu-map-api-key.md) | [Italiano](../../it/07-jetson-nano-agnss/baidu-map-api-key.md) | [日本語](../../ja/07-jetson-nano-agnss/baidu-map-api-key.md) | [한국어](../../ko/07-jetson-nano-agnss/baidu-map-api-key.md) | [Português (BR)](../../pt-br/07-jetson-nano-agnss/baidu-map-api-key.md) | [Português (PT)](../../pt-pt/07-jetson-nano-agnss/baidu-map-api-key.md) | [简体中文](../../zh-hans/07-jetson-nano-agnss/baidu-map-api-key.md) | [繁體中文](../../zh-hant/07-jetson-nano-agnss/baidu-map-api-key.md)

**Solicitud de una clave de API de Baidu Maps**

**1. Registro**

Ve a la plataforma abierta de Baidu Maps: <https://lbsyun.baidu.com/>

Desplázate hasta el final de la página y haz clic en «Register now».

![registro](../../en/07-jetson-nano-agnss/images/18.jpg)

Se recomienda registrarse como desarrollador individual, ya que la clave puede utilizarse el mismo día.

Sigue las indicaciones para completar el registro.

![pasos de registro](../../en/07-jetson-nano-agnss/images/19.jpg)

**2. Obtención del AK**

El servicio que se utiliza aquí es el servicio de localización por IP de la Web Service API. Su documentación está en:

<https://lbsyun.baidu.com/index.php?title=webapi/ip-api>

Haz clic en **Console**, elige **My Applications** y luego **Create Application**.

![consola](../../en/07-jetson-nano-agnss/images/20.jpg)

Pon a la aplicación el nombre que quieras, elige **Server side** como tipo de aplicación, activa el servicio e introduce `0.0.0.0/0` en la lista blanca.

![crear aplicación](../../en/07-jetson-nano-agnss/images/21.jpg)

Haz clic en **Submit** para crear la aplicación.

![enviado](../../en/07-jetson-nano-agnss/images/22.jpg)

Copia el valor AK de la aplicación.

![copiar ak](../../en/07-jetson-nano-agnss/images/23.jpg)

Pégalo en el programa y guarda: a continuación podrás leer la información de posición a través de Baidu Maps.

![pegar ak](../../en/07-jetson-nano-agnss/images/24.jpg)
