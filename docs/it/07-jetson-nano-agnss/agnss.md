[English](../../en/07-jetson-nano-agnss/agnss.md) | [Deutsch](../../de/07-jetson-nano-agnss/agnss.md) | [Español](../../es/07-jetson-nano-agnss/agnss.md) | [Français](../../fr/07-jetson-nano-agnss/agnss.md) | Italiano | [日本語](../../ja/07-jetson-nano-agnss/agnss.md) | [한국어](../../ko/07-jetson-nano-agnss/agnss.md) | [Português (BR)](../../pt-br/07-jetson-nano-agnss/agnss.md) | [Português (PT)](../../pt-pt/07-jetson-nano-agnss/agnss.md) | [简体中文](../../zh-hans/07-jetson-nano-agnss/agnss.md) | [繁體中文](../../zh-hant/07-jetson-nano-agnss/agnss.md)

**Posizionamento assistito AGNSS**

**1. Obiettivi**

In questa lezione utilizziamo un Jetson Orin, il modulo GPS e un server AGNSS per leggere e analizzare le informazioni di posizione in condizioni di segnale debole.

**2. Informazioni su AGNSS**

2.1 **Perché AGNSS**

- Un ricevitore GNSS autonomo deve acquisire e inseguire i segnali satellitari e decodificare il messaggio di navigazione prima di poter determinare la propria posizione.
- In un ambiente con segnale forte può avviarsi a freddo in circa 30 secondi. In un ambiente con segnale debole l'acquisizione è lenta e il messaggio di navigazione è difficile da decodificare, quindi il fix può richiedere molto tempo o non avvenire mai.
- AGNSS fornisce al ricevitore l'assistenza necessaria — dati di navigazione, una posizione approssimativa e l'ora. In entrambe le condizioni, con segnale forte o debole, riduce in modo significativo il tempo al primo fix (TTFF).

2.2 **Come funziona**

- Un server AGNSS raccoglie e gestisce i dati di assistenza provenienti da diverse fonti GNSS e risponde alle richieste dei client (che richiedono un nome utente e una password).
- Il client recupera i dati di assistenza tramite TCP/IP e li inoltra al ricevitore GNSS.
- È inoltre possibile eseguire un proprio server proxy.

![architettura](../../en/07-jetson-nano-agnss/images/1.png)

2.3 **Procedura**

- Connettersi al server AGNSS
  - Indirizzo: `121.41.40.95` (dominio `www.gnss-aide.com`)
  - Porta: `2621`
- Inviare una richiesta AGNSS
  - Stringa di richiesta (nome utente e password sono obbligatori):
  - `user=<your-username>;pwd=<your-password>;cmd=full;gnss=gps+bd;lat=60.0;lon=55.0;alt=0;`
- Ricevere i dati di assistenza
- Inoltrarli al ricevitore

2.4 **Parametri della richiesta**

La richiesta è una sequenza di coppie `key=value;`, ad esempio `key=value;key=value;`.

Esempio: `user=<your-username>;pwd=<your-password>;cmd=full;gnss=gps+bd;lat=60.0;lon=55.0;alt=0;`

| Chiave | Valore | Obbligatorio | Note |
| --- | --- | --- | --- |
| **user** | string | sì | Nome utente. Si raccomanda vivamente di usare un indirizzo email valido — su di esso vengono inviati importanti avvisi di manutenzione del server AGNSS. |
| **pwd** | string | sì | Password dell'utente |
| **gnss** | string | no | Elenco GNSS separato da virgole; attualmente è supportato il GPS. I valori validi sono `gps`, `bds`, `glo`. `gnss=gps;` richiede l'assistenza GPS, `gnss=gps,bds;` richiede l'assistenza GPS e BDS. |
| **cmd** | string | no | `full`: tutte le informazioni, incluse effemeridi, ora stimata e posizione. `eph`: solo effemeridi. `aid`: ora e posizione di assistenza. Il valore predefinito è `full`. |
| **lat** | number | no | Latitudine stimata dell'utente, in gradi (-90 a 90). L'assistenza di posizione è disponibile in due formati — lat/lon/alt oppure ECEF — e se ne sceglie uno. Il formato lat/lon/alt richiede tutti e tre i campi: `lat=30;lon=120.3;alt=100;` |
| **lon** | number | no | Longitudine stimata dell'utente, in gradi (-180 a 180). |
| **alt** | number | no | Altitudine stimata dell'utente, in metri. |
| **x** | number | no | Coordinata ECEF X stimata dell'utente, in metri. Il formato ECEF richiede tutti e tre i campi: `x=30000;y=1111120.3;z=3345100;` |
| **y** | number | no | Coordinata ECEF Y stimata dell'utente, in metri. |
| **z** | number | no | Coordinata ECEF Z stimata dell'utente, in metri. |
| **pacc** | number | no | Precisione della posizione dell'utente, in metri. |

2.5 **Risposta del server**

![risposta](../../en/07-jetson-nano-agnss/images/2.png)

- Il server restituisce un'intestazione dei dati seguita dai dati di assistenza.
- Il payload binario sono i dati di assistenza di cui il ricevitore ha bisogno e porta con sé il proprio checksum. Per il formato binario vedere la specifica del protocollo del ricevitore CASIC.
- Inoltrare al ricevitore anche l'intestazione è innocuo.

2.6 **Prestazioni**

Rispetto a un ricevitore GNSS autonomo, un ricevitore AGNSS migliora sensibilmente il TTFF, soprattutto in condizioni di segnale debole.

![confronto TTFF](../../en/07-jetson-nano-agnss/images/3.jpg)

2.7 **Note**

- La posizione approssimativa deve essere ottenuta in altro modo, ad esempio da:
  - un modulo GSM/GPRS/3G, che può ricavare una posizione approssimativa dal cell ID
  - Wi-Fi o un altro modulo wireless, che può anch'esso localizzare approssimativamente
- La posizione approssimativa deve essere accurata entro 15 km; un suggerimento di posizione errato peggiora le prestazioni del ricevitore.
- Se non è disponibile alcuna posizione approssimativa, omettere i campi di posizione (lat, lon, alt, x, y, z) dalla richiesta — il ricevitore ricade allora sulla sua ultima posizione valida.
- Non è necessario usare l'output del ricevitore stesso come posizione approssimativa.

2.8 **Quando è necessario AGNSS**

Non è necessario scaricare dal server a ogni avvio, il che fa risparmiare banda:

- I chip CASIC dispongono di una SRAM alimentata a batteria e di una flash di backup permanente che conservano i dati delle effemeridi ricevute.
- Durante il normale funzionamento il chip continua a scaricare le effemeridi più recenti dai satelliti.
- È possibile interrogare lo stato del ricevitore per decidere se è necessario un download. Il ricevitore può emettere una frase di stato del messaggio di navigazione (disattivata per impostazione predefinita; deve essere configurata).

2.9 **La frase di stato del messaggio di navigazione**

![frase 1](../../en/07-jetson-nano-agnss/images/4.png)

![frase 2](../../en/07-jetson-nano-agnss/images/5.png)

- Questa frase riporta l'ora interna del ricevitore e lo stato del messaggio di navigazione.
- Inviare `$PCAS03,,,,,,,,,,,1*1F` per emetterla una volta al secondo.
- Inviare `$PCAS03,,,,,,,,,,,0*1E` per interromperne l'emissione.
- Nota: ogni frase deve terminare con `\r\n` (0x0D, 0x0A) e contiene 11 virgole.
- Se il flag di ora è valido (diverso da zero) e il numero di effemeridi valide è elevato (più di 8), non è necessario scaricare le effemeridi AGNSS.

**3. Preparazione**

**3.1 Cablaggio**

Il modulo GPS supporta la comunicazione UART o USB; qui utilizziamo l'USB.

![cablaggio](../../en/07-jetson-nano-agnss/images/6.png)

Collegare il Jetson Orin al modulo GPS con un cavo Type-C, quindi eseguire `ls /dev | grep 'ttyUSB'` — il modulo viene rilevato come `USB0`.

![rilevamento del dispositivo](../../en/07-jetson-nano-agnss/images/7.jpg)

**3.2 Ottenere un AK di Baidu Maps**

Vedere [Richiesta di una chiave API di Baidu Maps](baidu-map-api-key.md).

**4. Programma**

Il programma di questa lezione è `GPS-agnss.py`.

Inizializzare l'USB:

![codice](../../en/07-jetson-nano-agnss/images/8.jpg)

Inserire l'AK richiesto; la latitudine e la longitudine approssimative correnti possono quindi essere lette da Baidu Maps.

![codice](../../en/07-jetson-nano-agnss/images/9.jpg)

Le coordinate approssimative di Baidu Maps vengono inviate al server — usare il proprio account AGNSS — e, una volta completato, l'intero pacchetto viene inviato al modulo.

![codice](../../en/07-jetson-nano-agnss/images/10.jpg)

![codice](../../en/07-jetson-nano-agnss/images/11.jpg)

La funzione di acquisizione e analisi della posizione filtra i dati in ingresso cercando le frasi che iniziano con `GNGGA` e le analizza in variabili globali.

![codice](../../en/07-jetson-nano-agnss/images/12.jpg)

![codice](../../en/07-jetson-nano-agnss/images/13.jpg)

Con lo stesso approccio si leggono e si analizzano le informazioni di rotta da `GNVTG`.

![codice](../../en/07-jetson-nano-agnss/images/14.jpg)

I dati analizzati vengono stampati in un ciclo continuo.

![codice](../../en/07-jetson-nano-agnss/images/15.jpg)

**5. Esecuzione del programma**

Eseguire `sudo python2 GPS-agnss.py` in un terminale.

**6. Risultato**

**Nota: con il posizionamento assistito il Jetson Orin deve disporre di accesso alla rete.**

Dopo l'accensione in un ambiente con segnale debole il programma inizializza l'USB e stampa `GPS Serial Opened! Baudrate=9600` in caso di successo, oppure `GPS Serial Open Failed!` in caso di errore — se fallisce, verificare il cablaggio o la porta USB.

Poi stampa `GPS Agnss start` mentre invia i dati di assistenza al server, e `GPS Agnss success` al termine.

Finché non viene acquisito un segnale GPS stampa `GPS no found` insieme alle coordinate approssimative lette da Baidu Maps.

![output](../../en/07-jetson-nano-agnss/images/16.jpg)

Una volta acquisito il segnale, stampa in un ciclo continuo le informazioni di posizione e rotta.

![output](../../en/07-jetson-nano-agnss/images/17.jpg)

Premere Ctrl+C per interrompere la lettura.
