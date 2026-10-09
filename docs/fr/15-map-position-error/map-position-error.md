[English](../../en/15-map-position-error/map-position-error.md) | [Deutsch](../../de/15-map-position-error/map-position-error.md) | [Español](../../es/15-map-position-error/map-position-error.md) | Français | [Italiano](../../it/15-map-position-error/map-position-error.md) | [日本語](../../ja/15-map-position-error/map-position-error.md) | [한국어](../../ko/15-map-position-error/map-position-error.md) | [Português (BR)](../../pt-br/15-map-position-error/map-position-error.md) | [Português (PT)](../../pt-pt/15-map-position-error/map-position-error.md) | [简体中文](../../zh-hans/15-map-position-error/map-position-error.md) | [繁體中文](../../zh-hant/15-map-position-error/map-position-error.md)

# Erreur de positionnement sur la carte

## Avant-propos

Tencent Maps et Amap utilisent un système de coordonnées différent de celui de l'outil hôte. Notre outil hôte appelle l'API Tianditu (WGS-84), les données converties diffèrent donc. Après avoir obtenu les données de position GPS / BeiDou, vous devez les convertir vers les coordonnées (WGS-84) de Tianditu avant toute autre utilisation.

## Systèmes de coordonnées courants

    WGS-84 (GPS)
    La norme internationale. Les coordonnées des appareils GPS standard, et celles utilisées par
    les fournisseurs de cartes internationaux, sont en WGS-84.

    GCJ-02
    La norme chinoise, publiée par le Bureau national de la cartographie en 2002.
    Également appelée « coordonnées Mars ». En Chine, une localisation géographique doit être
    chiffrée au moins une fois en GCJ-02. Google China, Amap et Tencent Maps l'utilisent tous.

    BD-09
    La norme de Baidu : un second chiffrement appliqué par-dessus GCJ-02.

![systèmes de coordonnées](../../en/15-map-position-error/images/1.png)

## Coordonnées BeiDou

Si vous avez déjà travaillé avec un système de positionnement BeiDou, vous avez peut-être remarqué quelque chose d'étrange : la latitude et la longitude semblent avoir été multipliées par 100.

```
$GNRMC,083735.000,A,2429.53531,N,11810.78036,E,0.54,171.11,190621,A*7E
```

C'est la valeur de coordonnée que rapporte le récepteur BeiDou : latitude `2429.53531` N, longitude `11810.78036` E. Si vous divisez simplement par 100, vous obtenez 24.2953531 N / 118.1078036 E — et la position est complètement fausse lorsqu'on la recherche dans Baidu ou Amap.

Amap :

![amap](../../en/15-map-position-error/images/2.png)

Baidu Maps :

![baidu](../../en/15-map-position-error/images/3.png)

Les deux sont décalées de dizaines de kilomètres. La raison est qu'en Chine, Amap comme Baidu utilisent des valeurs de latitude/longitude *chiffrées* plutôt que les coordonnées GPS brutes. Ainsi, pour utiliser des coordonnées BeiDou sur une carte commerciale, vous devez d'abord les passer par le chiffrement correspondant.

## Conversion entre systèmes de coordonnées

Tout d'abord, un point important : la valeur de coordonnée BeiDou **n'est pas** une simple relation ×100 — elle nécessite une conversion degrés-minutes. Pour une latitude `2429.53531` N et une longitude `11810.78036` E :

```
24 + (29.53531 / 60) ≈ 24.49225517
118 + (10.78036 / 60) ≈ 118.17967267
```

Ces deux valeurs sont celles que vous injectez dans les formules de conversion. Convertir directement depuis la valeur ×100 donne aussi une position fausse, alors convertissez d'abord en WGS-84.

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

WGS-84 vers GCJ-02 :

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

GCJ-02 vers BD-09 :

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

Autres fonctions utilitaires et constantes utilisées entre-temps :

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

Pour Amap, utilisez le résultat GCJ-02 ; pour Baidu Maps, utilisez le résultat BD-09.

## Résumé

Google Maps et similaires utilisent le système WGS-84. Les coordonnées BeiDou nécessitent une conversion degrés-minutes pour devenir WGS-84. Amap et similaires utilisent le système « Mars » GCJ-02, donc les coordonnées nécessitent un chiffrement GCJ-02 avant qu'Amap puisse les utiliser. Baidu Maps nécessite en plus un chiffrement BD-09 par-dessus.
