[English](../../en/15-map-position-error/map-position-error.md) | [Deutsch](../../de/15-map-position-error/map-position-error.md) | [Español](../../es/15-map-position-error/map-position-error.md) | [Français](../../fr/15-map-position-error/map-position-error.md) | Italiano | [日本語](../../ja/15-map-position-error/map-position-error.md) | [한국어](../../ko/15-map-position-error/map-position-error.md) | [Português (BR)](../../pt-br/15-map-position-error/map-position-error.md) | [Português (PT)](../../pt-pt/15-map-position-error/map-position-error.md) | [简体中文](../../zh-hans/15-map-position-error/map-position-error.md) | [繁體中文](../../zh-hant/15-map-position-error/map-position-error.md)

# Errore di posizionamento sulla mappa

## Premessa

Tencent Maps e Amap utilizzano un sistema di coordinate diverso da quello dello strumento host. Il nostro strumento host chiama l'API di Tianditu (WGS-84), quindi i dati convertiti differiscono. Dopo aver ottenuto i dati di posizione GPS / BeiDou bisogna convertirli nelle coordinate di Tianditu (WGS-84) prima di farne qualsiasi altra cosa.

## Sistemi di coordinate comuni

    WGS-84 (GPS)
    Lo standard internazionale. Le coordinate dei dispositivi GPS standard, e quelle usate
    dai fornitori di mappe internazionali, sono WGS-84.

    GCJ-02
    Lo standard cinese, pubblicato dall'Ufficio statale di rilevamento e mappatura nel 2002.
    Chiamato anche "coordinate di Marte". In Cina, una posizione geografica deve essere
    crittografata almeno una volta con GCJ-02. Google China, Amap e Tencent Maps lo usano tutti.

    BD-09
    Lo standard Baidu: una seconda crittografia applicata sopra GCJ-02.

![sistemi di coordinate](../../en/15-map-position-error/images/1.png)

## Coordinate BeiDou

Se hai già lavorato con un sistema di posizionamento BeiDou potresti aver notato qualcosa di strano: la latitudine e la longitudine sembrano essere state moltiplicate per 100.

```
$GNRMC,083735.000,A,2429.53531,N,11810.78036,E,0.54,171.11,190621,A*7E
```

Questo è il valore di coordinata riportato dal ricevitore BeiDou: latitudine `2429.53531` N, longitudine `11810.78036` E. Se si divide semplicemente per 100 si ottiene 24.2953531 N / 118.1078036 E — e la posizione è completamente sbagliata quando la si cerca in Baidu o Amap.

Amap:

![amap](../../en/15-map-position-error/images/2.png)

Baidu Maps:

![baidu](../../en/15-map-position-error/images/3.png)

Entrambe sono sbagliate di decine di chilometri. Il motivo è che in Cina sia Amap sia Baidu usano valori di latitudine/longitudine *crittografati* anziché le coordinate GPS grezze. Quindi per usare le coordinate BeiDou su una mappa commerciale bisogna prima farle passare attraverso la corrispondente crittografia.

## Conversione tra sistemi di coordinate

Innanzitutto un punto importante: il valore di coordinata BeiDou **non** ha una semplice relazione ×100 — richiede una conversione gradi-minuti. Per la latitudine `2429.53531` N e la longitudine `11810.78036` E:

```
24 + (29.53531 / 60) ≈ 24.49225517
118 + (10.78036 / 60) ≈ 118.17967267
```

Questi due valori sono quelli da inserire nelle formule di conversione. Convertire direttamente dal valore ×100 dà anch'esso una posizione errata, quindi convertire prima in WGS-84.

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

Da WGS-84 a GCJ-02:

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

Da GCJ-02 a BD-09:

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

Altre funzioni di supporto e costanti utilizzate nel mezzo:

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

Per Amap usare il risultato GCJ-02; per Baidu Maps usare il risultato BD-09.

## Riepilogo

Google Maps e simili usano il sistema WGS-84. Le coordinate BeiDou richiedono una conversione gradi-minuti per diventare WGS-84. Amap e simili usano il sistema GCJ-02 "Marte", quindi le coordinate richiedono una crittografia GCJ-02 prima che Amap possa usarle. Baidu Maps richiede un'ulteriore crittografia BD-09 sopra di essa.
