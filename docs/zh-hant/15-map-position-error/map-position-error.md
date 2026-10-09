[English](../../en/15-map-position-error/map-position-error.md) | [Deutsch](../../de/15-map-position-error/map-position-error.md) | [Español](../../es/15-map-position-error/map-position-error.md) | [Français](../../fr/15-map-position-error/map-position-error.md) | [Italiano](../../it/15-map-position-error/map-position-error.md) | [日本語](../../ja/15-map-position-error/map-position-error.md) | [한국어](../../ko/15-map-position-error/map-position-error.md) | [Português (BR)](../../pt-br/15-map-position-error/map-position-error.md) | [Português (PT)](../../pt-pt/15-map-position-error/map-position-error.md) | [简体中文](../../zh-hans/15-map-position-error/map-position-error.md) | 繁體中文

# 地圖定位誤差

[toc]

## 前言

騰訊，高德地圖使用的座標與上位機的座標不一樣，我們的上位機調用了天地圖的API（WGS-84標準），所以轉換出來的資料會有差異。在取得GPS/北斗定位資訊後，要把GPS/北斗的定位資訊轉化成天地圖（WGS-84標準）的座標之後再進行轉化。

## 常用座標系介紹

    WGS-84(GPS)
    國際標準，一般從國際標準的GPS設備取得的座標都是WGS-84，以及國際地圖提供商使用的座標系。
    
    GCJ-02
    中國標準，國測局02年發布的座標系。又稱“火星座標”。在中國，必須至少使用“GCJ-02”對地理位置進行首次加密。比如谷歌中國、高德、騰訊都在用這個座標系。
    
    BD-09
    百度標準，在“GCJ-02”的基礎上進行二次加密。

![image-202208160215](../../en/15-map-position-error/images/1.png)

## 北斗定位系統座標

如果有對接過北斗定位系統的小夥伴可能會發現一個問題，北斗座標經緯度好像都被乘了100？

$GNRMC,083735.000,A,2429.53531,N,11810.78036,E,0.54,171.11,190621,A*7E

這個，就是我們北斗定位系統接收到的座標值，可以發現，北緯是2429.53531，東經是11810.78036，倘若我們直接將這個經緯度除100，北緯24.2953531，東經118.1078036，在百度或者高德地圖中座標偏移的離譜。

高德地圖定位：
![image-202208160216](../../en/15-map-position-error/images/2.png)

百度地圖定位：

![image-202208160217](../../en/15-map-position-error/images/3.png)

可以發現，兩者的距離都偏移了幾十公里，這個原因就在於，國內，無論是高德還是百度，它們所使用的經緯度值，都是經過加密之後的值，而不是直接用GPS的實際經緯度來定位的，因此，我們如果想要將北斗定位系統的座標系，用於商業地圖上，則需要將它經過對應的加密轉換處理才能夠正確的使用。

## 座標系的相互轉換

首先，要強調一點，其實我們北斗定位的座標系值並不是簡單的100倍關係，而是需要做一次度分秒的轉換的。則我們取得的北斗座標值，北緯2429.53531，東經11810.78036，需要做如下計算：24+（29.53531/60）≈ 24.49225517 118+（10.78036/60）≈118.17967267

這兩個值才是我們應該帶入轉換公式的座標值，如果直接用100倍關係的值去轉換，定位一樣會偏差，所以需要先轉化為gps84標準的座標值。

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

WGS-84轉化成GCJ-02：


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

GCJ-02轉化成BD-09：

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

其他中間需要的函式和變數：

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

高德地圖請用的GCJ-02座標系轉換結果，百度座標系請用BD-09座標系轉換結果。

## 總結

谷歌地圖那些，用的是WGS-84座標系，北斗定位系統給到的座標值要做一次度分秒的轉換，轉換後才是84座標，像高德地圖那些用的是GCJ-02火星座標系，等於要先做一次GCJ-02加密，座標系才能在高德地圖用，百度地圖則需要再做一次BD-09的加密。
