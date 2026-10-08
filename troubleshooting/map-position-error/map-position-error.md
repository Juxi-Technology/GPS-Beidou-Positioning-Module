English | [简体中文](map-position-error_CN.md)

# Map Positioning Error

## Foreword

Tencent Maps and Amap use a different coordinate system from the host tool. Our host tool calls the Tianditu API (WGS-84), so the converted data differs. After getting GPS / BeiDou position data you have to convert it to Tianditu's (WGS-84) coordinates before doing anything else with it.

## Common coordinate systems

    WGS-84 (GPS)
    The international standard. Coordinates from standard GPS devices, and those used by
    international map providers, are WGS-84.

    GCJ-02
    The Chinese standard, published by the State Bureau of Surveying and Mapping in 2002.
    Also called the "Mars coordinates". Inside China, a geographic location must be
    encrypted with GCJ-02 at least once. Google China, Amap and Tencent Maps all use it.

    BD-09
    The Baidu standard: a second encryption applied on top of GCJ-02.

![coordinate systems](1.png)

## BeiDou coordinates

If you have worked with a BeiDou positioning system you may have noticed something odd: the latitude and longitude appear to have been multiplied by 100.

```
$GNRMC,083735.000,A,2429.53531,N,11810.78036,E,0.54,171.11,190621,A*7E
```

This is the coordinate value the BeiDou receiver reports: latitude `2429.53531` N, longitude `11810.78036` E. If you simply divide by 100 you get 24.2953531 N / 118.1078036 E — and the position is wildly off when looked up in Baidu or Amap.

Amap:

![amap](2.png)

Baidu Maps:

![baidu](3.png)

Both are off by tens of kilometres. The reason is that inside China both Amap and Baidu use *encrypted* latitude/longitude values rather than the raw GPS coordinates. So to use BeiDou coordinates on a commercial map you have to run them through the matching encryption first.

## Converting between coordinate systems

First, an important point: the BeiDou coordinate value is **not** a simple ×100 relationship — it needs a degrees-minutes conversion. For latitude `2429.53531` N and longitude `11810.78036` E:

```
24 + (29.53531 / 60) ≈ 24.49225517
118 + (10.78036 / 60) ≈ 118.17967267
```

Those two values are what you feed into the conversion formulas. Converting directly from the ×100 value also gives a wrong position, so convert to WGS-84 first.

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

WGS-84 to GCJ-02:

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

GCJ-02 to BD-09:

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

Other helper functions and constants used in between:

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

For Amap use the GCJ-02 result; for Baidu Maps use the BD-09 result.

## Summary

Google Maps and similar use the WGS-84 system. BeiDou coordinates need a degrees-minutes conversion to become WGS-84. Amap and similar use the GCJ-02 "Mars" system, so the coordinates need one GCJ-02 encryption before Amap can use them. Baidu Maps needs a further BD-09 encryption on top of that.
