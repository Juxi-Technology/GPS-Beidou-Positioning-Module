[English](../../en/15-map-position-error/map-position-error.md) | [Deutsch](../../de/15-map-position-error/map-position-error.md) | Español | [Français](../../fr/15-map-position-error/map-position-error.md) | [Italiano](../../it/15-map-position-error/map-position-error.md) | [日本語](../../ja/15-map-position-error/map-position-error.md) | [한국어](../../ko/15-map-position-error/map-position-error.md) | [Português (BR)](../../pt-br/15-map-position-error/map-position-error.md) | [Português (PT)](../../pt-pt/15-map-position-error/map-position-error.md) | [简体中文](../../zh-hans/15-map-position-error/map-position-error.md) | [繁體中文](../../zh-hant/15-map-position-error/map-position-error.md)

# Error de posicionamiento en el mapa

## Prefacio

Tencent Maps y Amap utilizan un sistema de coordenadas distinto del de la herramienta host. Nuestra herramienta host llama a la API de Tianditu (WGS-84), por lo que los datos convertidos difieren. Después de obtener los datos de posición de GPS / BeiDou, hay que convertirlos a las coordenadas de Tianditu (WGS-84) antes de hacer cualquier otra cosa con ellos.

## Sistemas de coordenadas habituales

    WGS-84 (GPS)
    El estándar internacional. Las coordenadas de los dispositivos GPS estándar, y las
    que utilizan los proveedores de mapas internacionales, son WGS-84.

    GCJ-02
    El estándar chino, publicado por la Oficina Estatal de Topografía y Cartografía en 2002.
    También se conoce como «coordenadas Marte». Dentro de China, una ubicación geográfica debe
    cifrarse con GCJ-02 al menos una vez. Google China, Amap y Tencent Maps lo utilizan.

    BD-09
    El estándar de Baidu: un segundo cifrado aplicado sobre GCJ-02.

![sistemas de coordenadas](../../en/15-map-position-error/images/1.png)

## Coordenadas de BeiDou

Si has trabajado con un sistema de posicionamiento BeiDou, es posible que hayas notado algo raro: parece que la latitud y la longitud se han multiplicado por 100.

```
$GNRMC,083735.000,A,2429.53531,N,11810.78036,E,0.54,171.11,190621,A*7E
```

Este es el valor de coordenadas que informa el receptor BeiDou: latitud `2429.53531` N, longitud `11810.78036` E. Si simplemente divides entre 100 obtienes 24.2953531 N / 118.1078036 E, y la posición queda muy desviada al buscarla en Baidu o Amap.

Amap:

![amap](../../en/15-map-position-error/images/2.png)

Baidu Maps:

![baidu](../../en/15-map-position-error/images/3.png)

Ambos están desviados decenas de kilómetros. El motivo es que, dentro de China, tanto Amap como Baidu utilizan valores de latitud/longitud *cifrados* en lugar de las coordenadas GPS sin procesar. Por lo tanto, para usar coordenadas BeiDou en un mapa comercial hay que pasarlas primero por el cifrado correspondiente.

## Conversión entre sistemas de coordenadas

En primer lugar, un punto importante: el valor de coordenadas BeiDou **no** guarda una relación simple de ×100; necesita una conversión de grados y minutos. Para la latitud `2429.53531` N y la longitud `11810.78036` E:

```
24 + (29.53531 / 60) ≈ 24.49225517
118 + (10.78036 / 60) ≈ 118.17967267
```

Esos dos valores son los que se introducen en las fórmulas de conversión. Convertir directamente a partir del valor ×100 también da una posición errónea, así que convierte primero a WGS-84.

```python
def str_To_Gps84(self, in_data1, in_data2):
    len_data1 = len(in_data1)
    str_data2 = "%05d" % int(in_data2)
    temp_data = int(in_data1)
    symbol = 1
    if temp_data < 0:
        symbol = -1
    degree = int(temp_data / 100.0)
    str_decimal = str(in_data1[len_data1-2]) + str(in_data1[len_data1-1]) + '.' + str(str_data2)
    f_degree = float(str_decimal)/60.0
    # print("f_degree:", f_degree)
    if symbol > 0:
        result = degree + f_degree
    else:
        result = degree - f_degree
    return result
```

De WGS-84 a GCJ-02:

```python
def gps84_to_gcj02(self, lat, lon):
    if (self.outOfChina(lat, lon)):
        return [0, 0]
    dLat = self.transformLat(lon - 105.0, lat - 35.0)
    dLon = self.transformLon(lon - 105.0, lat - 35.0)
    radLat = lat / 180.0 * self.PI
    magic = math.sin(radLat)
    magic = 1 - self.EE * magic * magic
    sqrtMagic = math.sqrt(magic)
    dLat = (dLat * 180.0)/((self.A * (1 - self.EE))/(magic * sqrtMagic) * self.PI)
    dLon = (dLon * 180.0) / (self.A / sqrtMagic * math.cos(radLat) * self.PI)
    mgLat = lat + dLat
    mgLon = lon + dLon
    return [mgLat, mgLon]
```

De GCJ-02 a BD-09:

```python
def gcj02_to_bd09(self, gg_lat, gg_lon):
    x = gg_lon
    y = gg_lat
    z = math.sqrt(x * x + y * y) + 0.00002 * math.sin(y * self.PI)
    theta = math.atan2(y, x) + 0.000003 * math.cos(x * self.PI)
    bd_lon = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    return [bd_lat, bd_lon]
```

Otras funciones auxiliares y constantes utilizadas entremedias:

```python
self.PI = 3.1415926535897932384626
self.A = 6378245.0
self.EE = 0.00669342162296594323

def outOfChina(self, lat, lon):
    if (lon < 72.004 or lon > 137.8347):
        return True
    if (lat < 0.8293 or lat > 55.8271):
        return True
    return False

def transform(self, lat, lon):
    if (self.outOfChina(lat, lon)):
        return [lat, lon]
    dLat = self.transformLat(lon - 105.0, lat - 35.0)
    dLon = self.transformLon(lon - 105.0, lat - 35.0)
    radLat = lat / 180.0 * self.PI
    magic = math.sin(radLat)
    magic = 1 - self.EE * magic * magic
    sqrtMagic = math.sqrt(magic)
    dLat = (dLat * 180.0) / ((self.A * (1 - self.EE)) / (magic * sqrtMagic) *self.PI)
    dLon = (dLon * 180.0) / (self.A / sqrtMagic * math.cos(radLat) * self.PI)
    mgLat = lat + dLat
    mgLon = lon + dLon
    return [mgLat, mgLon]

def transformLat(self, x, y):
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * self.PI) + 20.0 * math.sin(2.0 * x * self.PI)) * 2.0 / 3.0
    ret += (20.0 * math.sin(y * self.PI) + 40.0 * math.sin(y / 3.0 * self.PI)) * 2.0 / 3.0
    ret += (160.0 * math.sin(y / 12.0 * self.PI) + 320 * math.sin(y * self.PI / 30.0)) * 2.0 / 3.0
    return ret

def transformLon(self, x, y):
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * self.PI) + 20.0 * math.sin(2.0 * x * self.PI)) * 2.0 / 3.0
    ret += (20.0 * math.sin(x * self.PI) + 40.0 * math.sin(x / 3.0 * self.PI)) * 2.0 / 3.0
    ret += (150.0 * math.sin(x / 12.0 * self.PI) + 300.0 * math.sin(x / 30.0 * self.PI)) * 2.0 / 3.0
    return ret
```

Para Amap, usa el resultado GCJ-02; para Baidu Maps, usa el resultado BD-09.

## Resumen

Google Maps y similares utilizan el sistema WGS-84. Las coordenadas BeiDou necesitan una conversión de grados y minutos para convertirse en WGS-84. Amap y similares utilizan el sistema GCJ-02 «Marte», por lo que las coordenadas necesitan un cifrado GCJ-02 antes de que Amap pueda usarlas. Baidu Maps necesita además un cifrado BD-09 sobre aquel.
