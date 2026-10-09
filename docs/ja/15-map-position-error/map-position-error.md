[English](../../en/15-map-position-error/map-position-error.md) | [Deutsch](../../de/15-map-position-error/map-position-error.md) | [Español](../../es/15-map-position-error/map-position-error.md) | [Français](../../fr/15-map-position-error/map-position-error.md) | [Italiano](../../it/15-map-position-error/map-position-error.md) | 日本語 | [한국어](../../ko/15-map-position-error/map-position-error.md) | [Português (BR)](../../pt-br/15-map-position-error/map-position-error.md) | [Português (PT)](../../pt-pt/15-map-position-error/map-position-error.md) | [简体中文](../../zh-hans/15-map-position-error/map-position-error.md) | [繁體中文](../../zh-hant/15-map-position-error/map-position-error.md)

# 地図上の測位誤差

## はじめに

Tencent Maps と Amap は、ホストツールとは異なる座標系を使用しています。当社のホストツールは天地図（Tianditu）の API（WGS-84）を呼び出すため、変換後のデータが異なります。GPS／北斗の測位データを取得したら、他の処理を行う前に、天地図（WGS-84）の座標系に変換する必要があります。

## 一般的な座標系

    WGS-84（GPS）
    国際標準です。標準的な GPS 機器から得られる座標、および国際的な地図プロバイダーが
    使用する座標は WGS-84 です。

    GCJ-02
    中国標準で、2002 年に国家測絵局（State Bureau of Surveying and Mapping）が公布しました。
    「火星座標」とも呼ばれます。中国国内では、地理的位置は少なくとも 1 回
    GCJ-02 で暗号化する必要があります。Google China、Amap、Tencent Maps はいずれもこれを使用します。

    BD-09
    Baidu 標準：GCJ-02 の上にさらに施される 2 回目の暗号化です。

![座標系](../../en/15-map-position-error/images/1.png)

## 北斗の座標

北斗の測位システムを扱ったことがある方は、奇妙な点に気づいたかもしれません。緯度と経度が 100 倍されているように見えるのです。

```
$GNRMC,083735.000,A,2429.53531,N,11810.78036,E,0.54,171.11,190621,A*7E
```

これが北斗受信機の報告する座標値です。緯度 `2429.53531` N、経度 `11810.78036` E です。これを単純に 100 で割ると 24.2953531 N / 118.1078036 E になり、Baidu や Amap で調べると位置が大幅にずれます。

Amap：

![amap](../../en/15-map-position-error/images/2.png)

Baidu Maps：

![baidu](../../en/15-map-position-error/images/3.png)

どちらも数十キロメートルずれています。その理由は、中国国内では Amap も Baidu も生の GPS 座標ではなく、*暗号化された*緯度・経度の値を使用しているためです。したがって、北斗の座標を商用地図で使用するには、まず対応する暗号化を施す必要があります。

## 座標系間の変換

まず重要な点です。北斗の座標値は**単純な 100 倍の関係ではなく**、度分変換が必要です。緯度 `2429.53531` N、経度 `11810.78036` E の場合：

```
24 + (29.53531 / 60) ≈ 24.49225517
118 + (10.78036 / 60) ≈ 118.17967267
```

この 2 つの値が変換式に与える値です。100 倍の値から直接変換しても位置がずれるため、まず WGS-84 に変換してください。

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

WGS-84 から GCJ-02 へ：

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

GCJ-02 から BD-09 へ：

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

途中で使用されるその他のヘルパー関数と定数：

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

Amap には GCJ-02 の結果を、Baidu Maps には BD-09 の結果を使用します。

## まとめ

Google Maps などは WGS-84 システムを使用しています。北斗の座標は度分変換を行って WGS-84 にする必要があります。Amap などは GCJ-02 の「火星」システムを使用しているため、Amap が使用できるようになる前に座標を 1 回 GCJ-02 で暗号化する必要があります。Baidu Maps はその上にさらに BD-09 の暗号化が必要です。
