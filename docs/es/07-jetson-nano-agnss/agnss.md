[English](../../en/07-jetson-nano-agnss/agnss.md) | [Deutsch](../../de/07-jetson-nano-agnss/agnss.md) | Español | [Français](../../fr/07-jetson-nano-agnss/agnss.md) | [Italiano](../../it/07-jetson-nano-agnss/agnss.md) | [日本語](../../ja/07-jetson-nano-agnss/agnss.md) | [한국어](../../ko/07-jetson-nano-agnss/agnss.md) | [Português (BR)](../../pt-br/07-jetson-nano-agnss/agnss.md) | [Português (PT)](../../pt-pt/07-jetson-nano-agnss/agnss.md) | [简体中文](../../zh-hans/07-jetson-nano-agnss/agnss.md) | [繁體中文](../../zh-hant/07-jetson-nano-agnss/agnss.md)

**Posicionamiento asistido AGNSS**

**1. Objetivos**

En esta lección utilizamos un Jetson Orin, el módulo GPS y un servidor AGNSS para leer y analizar la información de posición en condiciones de señal débil.

**2. Acerca de AGNSS**

2.1 **Por qué AGNSS**

- Un receptor GNSS autónomo debe adquirir y seguir las señales de los satélites y decodificar el mensaje de navegación antes de poder fijar su posición.
- En un entorno con buena señal puede arrancar en frío en unos 30 segundos. En un entorno con señal débil, la adquisición es lenta y el mensaje de navegación es difícil de decodificar, por lo que obtener un fix puede tardar muchísimo o no llegar a producirse nunca.
- AGNSS proporciona al receptor la asistencia que necesita: datos de navegación, una posición aproximada y la hora. Tanto con buena señal como con señal débil, esto reduce notablemente el tiempo hasta el primer fix (TTFF).

2.2 **Cómo funciona**

- Un servidor AGNSS recopila y gestiona datos de asistencia de varias fuentes GNSS, y responde a las solicitudes de los clientes (que requieren un nombre de usuario y una contraseña).
- El cliente obtiene los datos de asistencia por TCP/IP y los reenvía al receptor GNSS.
- También puedes ejecutar tu propio servidor proxy.

![arquitectura](../../en/07-jetson-nano-agnss/images/1.png)

2.3 **Procedimiento**

- Conéctate al servidor AGNSS
  - Dirección: `121.41.40.95` (dominio `www.gnss-aide.com`)
  - Puerto: `2621`
- Envía una solicitud AGNSS
  - Cadena de solicitud (se requieren nombre de usuario y contraseña):
  - `user=<your-username>;pwd=<your-password>;cmd=full;gnss=gps+bd;lat=60.0;lon=55.0;alt=0;`
- Recibe los datos de asistencia
- Reenvíalos al receptor

2.4 **Parámetros de la solicitud**

La solicitud es una secuencia de pares `key=value;`, por ejemplo `key=value;key=value;`.

Ejemplo: `user=<your-username>;pwd=<your-password>;cmd=full;gnss=gps+bd;lat=60.0;lon=55.0;alt=0;`

| Clave | Valor | Obligatorio | Notas |
| --- | --- | --- | --- |
| **user** | cadena | sí | Nombre de usuario. Se recomienda encarecidamente usar una dirección de correo electrónico válida: ahí se envían los avisos importantes de mantenimiento del servidor AGNSS. |
| **pwd** | cadena | sí | Contraseña del usuario |
| **gnss** | cadena | no | Lista de sistemas GNSS separados por comas; actualmente se admite GPS. Los valores válidos son `gps`, `bds`, `glo`. `gnss=gps;` solicita asistencia para GPS; `gnss=gps,bds;` solicita asistencia para GPS y BDS. |
| **cmd** | cadena | no | `full`: toda la información, incluidos efemérides, hora y posición estimadas. `eph`: solo efemérides. `aid`: hora y posición de asistencia. Por defecto, `full`. |
| **lat** | número | no | Latitud estimada del usuario, en grados (-90 a 90). La asistencia de posición admite dos formatos —lat/lon/alt o ECEF— y hay que elegir uno. El formato lat/lon/alt requiere los tres campos: `lat=30;lon=120.3;alt=100;` |
| **lon** | número | no | Longitud estimada del usuario, en grados (-180 a 180). |
| **alt** | número | no | Altitud estimada del usuario, en metros. |
| **x** | número | no | Coordenada X estimada del usuario en ECEF, en metros. El formato ECEF requiere los tres campos: `x=30000;y=1111120.3;z=3345100;` |
| **y** | número | no | Coordenada Y estimada del usuario en ECEF, en metros. |
| **z** | número | no | Coordenada Z estimada del usuario en ECEF, en metros. |
| **pacc** | número | no | Precisión de la posición del usuario, en metros. |

2.5 **Respuesta del servidor**

![respuesta](../../en/07-jetson-nano-agnss/images/2.png)

- El servidor devuelve una cabecera de datos seguida de los datos de asistencia.
- La carga útil binaria son los datos de asistencia que necesita el receptor y lleva su propia suma de comprobación. Para conocer el formato binario, consulta la especificación del protocolo del receptor CASIC.
- Reenviar también la cabecera al receptor no supone ningún problema.

2.6 **Rendimiento**

En comparación con un receptor GNSS autónomo, un receptor AGNSS mejora el TTFF de forma notable, sobre todo en condiciones de señal débil.

![comparación de TTFF](../../en/07-jetson-nano-agnss/images/3.jpg)

2.7 **Notas**

- La posición aproximada debe obtenerse por otro medio, por ejemplo a partir de:
  - un módulo GSM/GPRS/3G, que puede deducir una posición aproximada a partir del ID de celda
  - Wi-Fi u otro módulo inalámbrico, que también puede localizar de forma aproximada
- La posición aproximada debe tener una exactitud de 15 km como máximo; una pista de posición errónea degrada el rendimiento del receptor.
- Si no se dispone de una posición aproximada, omite los campos de posición (lat, lon, alt, x, y, z) de la solicitud: el receptor recurrirá entonces a su último fix válido.
- No es necesario usar la propia salida del receptor como posición aproximada.

2.8 **Cuándo se necesita AGNSS**

No es necesario descargar del servidor en cada arranque, lo que ahorra ancho de banda:

- Los chips CASIC disponen de una SRAM con respaldo de batería y una flash de respaldo permanente que conservan los datos de efemérides recibidos.
- Durante el funcionamiento normal, el chip sigue descargando las últimas efemérides de los satélites.
- Puedes consultar el estado del receptor para decidir si es necesario descargar. El receptor puede emitir una sentencia de estado del mensaje de navegación (desactivada por defecto; hay que configurarla).

2.9 **La sentencia de estado del mensaje de navegación**

![sentencia 1](../../en/07-jetson-nano-agnss/images/4.png)

![sentencia 2](../../en/07-jetson-nano-agnss/images/5.png)

- Esta sentencia informa de la hora interna del receptor y del estado del mensaje de navegación.
- Envía `$PCAS03,,,,,,,,,,,1*1F` para que se emita una vez por segundo.
- Envía `$PCAS03,,,,,,,,,,,0*1E` para dejar de emitirla.
- Nota: toda sentencia debe terminar con `\r\n` (0x0D, 0x0A) y contiene 11 comas.
- Si el indicador de hora es válido (distinto de cero) y el número de efemérides válidas es elevado (más de 8), no es necesario descargar efemérides AGNSS.

**3. Preparación**

**3.1 Cableado**

El módulo GPS admite comunicación por UART o por USB; aquí usamos USB.

![cableado](../../en/07-jetson-nano-agnss/images/6.png)

Conecta el Jetson Orin al módulo GPS con un cable Type-C y ejecuta `ls /dev | grep 'ttyUSB'`: el módulo se detecta como `USB0`.

![detección del dispositivo](../../en/07-jetson-nano-agnss/images/7.jpg)

**3.2 Obtención de un AK de Baidu Maps**

Consulta [Solicitud de una clave de API de Baidu Maps](baidu-map-api-key.md).

**4. Programa**

El programa de esta lección es `GPS-agnss.py`.

Inicializa el USB:

![código](../../en/07-jetson-nano-agnss/images/8.jpg)

Rellena el AK que hayas solicitado y, a continuación, podrás leer la latitud y la longitud aproximadas actuales desde Baidu Maps.

![código](../../en/07-jetson-nano-agnss/images/9.jpg)

Las coordenadas aproximadas de Baidu Maps se envían al servidor (usa tu propia cuenta de AGNSS) y, una vez completado, el paquete entero se envía al módulo.

![código](../../en/07-jetson-nano-agnss/images/10.jpg)

![código](../../en/07-jetson-nano-agnss/images/11.jpg)

La función de adquisición y análisis de posición filtra los datos entrantes en busca de sentencias que empiezan por `GNGGA` y las analiza para volcarlas en variables globales.

![código](../../en/07-jetson-nano-agnss/images/12.jpg)

![código](../../en/07-jetson-nano-agnss/images/13.jpg)

Con el mismo enfoque se lee y analiza la información de rumbo procedente de `GNVTG`.

![código](../../en/07-jetson-nano-agnss/images/14.jpg)

Los datos analizados se imprimen en bucle.

![código](../../en/07-jetson-nano-agnss/images/15.jpg)

**5. Ejecución del programa**

Ejecuta `sudo python2 GPS-agnss.py` en un terminal.

**6. Resultado**

**Nota: con posicionamiento asistido, el Jetson Orin debe tener acceso a la red.**

Tras el encendido en un entorno de señal débil, el programa inicializa el USB e imprime `GPS Serial Opened! Baudrate=9600` si tiene éxito, o `GPS Serial Open Failed!` si falla; en ese caso, comprueba el cableado o el puerto USB.

A continuación imprime `GPS Agnss start` mientras envía los datos de asistencia al servidor, y `GPS Agnss success` cuando termina.

Hasta que se adquiere la señal GPS, imprime `GPS no found` junto con las coordenadas aproximadas leídas de Baidu Maps.

![salida](../../en/07-jetson-nano-agnss/images/16.jpg)

Una vez adquirida la señal, imprime la información de posición y de rumbo en bucle.

![salida](../../en/07-jetson-nano-agnss/images/17.jpg)

Pulsa Ctrl+C para detener la lectura.
