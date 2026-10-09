[English](../../en/15-map-position-error/map-position-error.md) | [Deutsch](../../de/15-map-position-error/map-position-error.md) | [Español](../../es/15-map-position-error/map-position-error.md) | [Français](../../fr/15-map-position-error/map-position-error.md) | [Italiano](../../it/15-map-position-error/map-position-error.md) | [日本語](../../ja/15-map-position-error/map-position-error.md) | [한국어](../../ko/15-map-position-error/map-position-error.md) | Português (BR) | [Português (PT)](../../pt-pt/15-map-position-error/map-position-error.md) | [简体中文](../../zh-hans/15-map-position-error/map-position-error.md) | [繁體中文](../../zh-hant/15-map-position-error/map-position-error.md)

# Erro de posicionamento no mapa

## Prefácio

O Tencent Maps e o Amap usam um sistema de coordenadas diferente do da ferramenta host. Nossa ferramenta host chama a API do Tianditu (WGS-84), então os dados convertidos diferem. Depois de obter os dados de posição do GPS / BeiDou, você precisa convertê-los para as coordenadas do Tianditu (WGS-84) antes de fazer qualquer outra coisa com eles.

## Sistemas de coordenadas comuns

    WGS-84 (GPS)
    The international standard. Coordinates from standard GPS devices, and those used by
    international map providers, are WGS-84.

    GCJ-02
    The Chinese standard, published by the State Bureau of Surveying and Mapping in 2002.
    Also called the "Mars coordinates". Inside China, a geographic location must be
    encrypted with GCJ-02 at least once. Google China, Amap and Tencent Maps all use it.

    BD-09
    The Baidu standard: a second encryption applied on top of GCJ-02.

![sistemas de coordenadas](../../en/15-map-position-error/images/1.png)

## Coordenadas do BeiDou

Se você já trabalhou com um sistema de posicionamento BeiDou, talvez tenha notado algo estranho: a latitude e a longitude parecem ter sido multiplicadas por 100.

```
$GNRMC,083735.000,A,2429.53531,N,11810.78036,E,0.54,171.11,190621,A*7E
```

Este é o valor de coordenada que o receptor BeiDou informa: latitude `2429.53531` N, longitude `11810.78036` E. Se você simplesmente dividir por 100, obtém 24.2953531 N / 118.1078036 E — e a posição fica totalmente errada quando consultada no Baidu ou no Amap.

Amap:

![amap](../../en/15-map-position-error/images/2.png)

Baidu Maps:

![baidu](../../en/15-map-position-error/images/3.png)

Ambos erram por dezenas de quilômetros. O motivo é que, dentro da China, tanto o Amap quanto o Baidu usam valores de latitude/longitude *criptografados* em vez das coordenadas brutas do GPS. Portanto, para usar coordenadas do BeiDou em um mapa comercial, você precisa antes passá-las pela criptografia correspondente.

## Conversão entre sistemas de coordenadas

Primeiro, um ponto importante: o valor de coordenada do BeiDou **não** tem uma relação simples de ×100 — ele precisa de uma conversão de graus-minutos. Para a latitude `2429.53531` N e a longitude `11810.78036` E:

```
24 + (29.53531 / 60) ≈ 24.49225517
118 + (10.78036 / 60) ≈ 118.17967267
```

Esses dois valores são o que você alimenta nas fórmulas de conversão. Converter diretamente a partir do valor ×100 também dá uma posição errada, então converta para WGS-84 primeiro.

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

De WGS-84 para GCJ-02:

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

De GCJ-02 para BD-09:

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

Outras funções auxiliares e constantes usadas no meio:

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

Para o Amap use o resultado GCJ-02; para o Baidu Maps use o resultado BD-09.

## Resumo

O Google Maps e afins usam o sistema WGS-84. As coordenadas do BeiDou precisam de uma conversão de graus-minutos para se tornarem WGS-84. O Amap e afins usam o sistema "Mars" GCJ-02, então as coordenadas precisam de uma criptografia GCJ-02 antes que o Amap possa usá-las. O Baidu Maps precisa de mais uma criptografia BD-09 em cima disso.
