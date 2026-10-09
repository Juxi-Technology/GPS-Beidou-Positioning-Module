[English](../../en/15-map-position-error/map-position-error.md) | [Deutsch](../../de/15-map-position-error/map-position-error.md) | [Español](../../es/15-map-position-error/map-position-error.md) | [Français](../../fr/15-map-position-error/map-position-error.md) | [Italiano](../../it/15-map-position-error/map-position-error.md) | [日本語](../../ja/15-map-position-error/map-position-error.md) | 한국어 | [Português (BR)](../../pt-br/15-map-position-error/map-position-error.md) | [Português (PT)](../../pt-pt/15-map-position-error/map-position-error.md) | [简体中文](../../zh-hans/15-map-position-error/map-position-error.md) | [繁體中文](../../zh-hant/15-map-position-error/map-position-error.md)

# 지도 측위 오차

## 머리말

Tencent Maps와 Amap은 호스트 도구와 다른 좌표계를 사용합니다. 호스트 도구는 Tianditu API(WGS-84)를 호출하므로 변환된 데이터가 다릅니다. GPS / BeiDou 위치 데이터를 얻은 후에는 다른 작업을 하기 전에 먼저 Tianditu(WGS-84) 좌표로 변환해야 합니다.

## 일반적인 좌표계

    WGS-84 (GPS)
    국제 표준입니다. 표준 GPS 기기의 좌표와 국제 지도 제공자가 사용하는 좌표가
    WGS-84입니다.

    GCJ-02
    중국 표준으로, 2002년 국가측량제도국이 공표했습니다. "화성 좌표"라고도
    합니다. 중국 내에서는 지리적 위치를 최소 한 번 GCJ-02로 암호화해야 합니다.
    Google China, Amap, Tencent Maps가 모두 이를 사용합니다.

    BD-09
    Baidu 표준으로, GCJ-02 위에 한 번 더 암호화를 적용한 것입니다.

![좌표계](../../en/15-map-position-error/images/1.png)

## BeiDou 좌표

BeiDou 측위 시스템을 사용해 본 적이 있다면 이상한 점을 눈치챘을 수 있습니다. 위도와 경도에 100이 곱해진 것처럼 보입니다.

```
$GNRMC,083735.000,A,2429.53531,N,11810.78036,E,0.54,171.11,190621,A*7E
```

이것은 BeiDou 수신기가 보고하는 좌표 값입니다: 위도 `2429.53531` N, 경도 `11810.78036` E. 단순히 100으로 나누면 24.2953531 N / 118.1078036 E가 되지만, Baidu나 Amap에서 조회하면 위치가 크게 어긋납니다.

Amap:

![amap](../../en/15-map-position-error/images/2.png)

Baidu Maps:

![baidu](../../en/15-map-position-error/images/3.png)

둘 다 수십 킬로미터나 어긋납니다. 그 이유는 중국 내에서 Amap과 Baidu 모두 원시 GPS 좌표가 아니라 *암호화된* 위도/경도 값을 사용하기 때문입니다. 따라서 BeiDou 좌표를 상용 지도에서 사용하려면 먼저 해당 암호화를 거쳐야 합니다.

## 좌표계 간 변환

먼저 중요한 점 하나: BeiDou 좌표 값은 단순한 ×100 관계가 **아니며**, 도-분 변환이 필요합니다. 위도 `2429.53531` N, 경도 `11810.78036` E인 경우:

```
24 + (29.53531 / 60) ≈ 24.49225517
118 + (10.78036 / 60) ≈ 118.17967267
```

이 두 값이 변환 공식에 입력하는 값입니다. ×100 값에서 직접 변환해도 위치가 잘못 나오므로, 먼저 WGS-84로 변환하십시오.

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

WGS-84에서 GCJ-02로:

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

GCJ-02에서 BD-09로:

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

중간에 사용되는 기타 헬퍼 함수와 상수:

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

Amap에는 GCJ-02 결과를, Baidu Maps에는 BD-09 결과를 사용합니다.

## 요약

Google Maps 등은 WGS-84 체계를 사용합니다. BeiDou 좌표는 도-분 변환을 거쳐야 WGS-84가 됩니다. Amap 등은 GCJ-02 "화성" 체계를 사용하므로, Amap이 사용할 수 있으려면 좌표를 한 번 GCJ-02로 암호화해야 합니다. Baidu Maps는 그 위에 BD-09 암호화를 한 번 더 필요로 합니다.
