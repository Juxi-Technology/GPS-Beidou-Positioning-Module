[English](../../en/09-raspberry-pi-agnss/agnss.md) | [Deutsch](../../de/09-raspberry-pi-agnss/agnss.md) | [Español](../../es/09-raspberry-pi-agnss/agnss.md) | Français | [Italiano](../../it/09-raspberry-pi-agnss/agnss.md) | [日本語](../../ja/09-raspberry-pi-agnss/agnss.md) | [한국어](../../ko/09-raspberry-pi-agnss/agnss.md) | [Português (BR)](../../pt-br/09-raspberry-pi-agnss/agnss.md) | [Português (PT)](../../pt-pt/09-raspberry-pi-agnss/agnss.md) | [简体中文](../../zh-hans/09-raspberry-pi-agnss/agnss.md) | [繁體中文](../../zh-hant/09-raspberry-pi-agnss/agnss.md)

**Positionnement assisté AGNSS**

**1. Objectifs**

Dans cette leçon, nous utilisons un Raspberry Pi, le module GPS et un serveur AGNSS pour lire et analyser les informations de position dans des conditions de signal faible.

**2. À propos de l'AGNSS**

2.1 **Pourquoi l'AGNSS**

- Un récepteur GNSS autonome doit acquérir et suivre les signaux satellites et décoder le message de navigation avant de pouvoir déterminer sa position.
- Dans un environnement à signal fort, il peut démarrer à froid en environ 30 secondes. Dans un environnement à signal faible, l'acquisition est lente et le message de navigation est difficile à décoder, si bien qu'un fix peut prendre très longtemps ou ne jamais se produire.
- L'AGNSS fournit au récepteur l'assistance dont il a besoin — données de navigation, position approximative et heure. Dans des conditions de signal fort comme faible, cela raccourcit sensiblement le temps jusqu'au premier fix (TTFF).

2.2 **Fonctionnement**

- Un serveur AGNSS collecte et gère les données d'assistance de plusieurs sources GNSS, et répond aux requêtes des clients (qui nécessitent un nom d'utilisateur et un mot de passe).
- Le client récupère les données d'assistance via TCP/IP et les transmet au récepteur GNSS.
- Vous pouvez également exécuter votre propre serveur proxy.

![architecture](../../en/09-raspberry-pi-agnss/images/1.png)

2.3 **Procédure**

- Se connecter au serveur AGNSS
  - Adresse : `121.41.40.95` (domaine `www.gnss-aide.com`)
  - Port : `2621`
- Envoyer une requête AGNSS
  - Chaîne de requête (nom d'utilisateur et mot de passe requis) :
  - `user=<your-username>;pwd=<your-password>;cmd=full;gnss=gps+bd;lat=60.0;lon=55.0;alt=0;`
- Recevoir les données d'assistance
- Les transmettre au récepteur

2.4 **Paramètres de la requête**

La requête est une suite de paires `key=value;`, par exemple `key=value;key=value;`.

Exemple : `user=<your-username>;pwd=<your-password>;cmd=full;gnss=gps+bd;lat=60.0;lon=55.0;alt=0;`

| Clé | Valeur | Requis | Remarques |
| --- | --- | --- | --- |
| **user** | string | yes | Nom d'utilisateur. Il est fortement recommandé d'utiliser une adresse e-mail valide — les avis importants de maintenance du serveur AGNSS y sont envoyés. |
| **pwd** | string | yes | Mot de passe utilisateur |
| **gnss** | string | no | Liste GNSS séparée par des virgules ; actuellement, le GPS est pris en charge. Les valeurs valides sont `gps`, `bds`, `glo`. `gnss=gps;` demande l'assistance GPS, `gnss=gps,bds;` demande l'assistance GPS et BDS. |
| **cmd** | string | no | `full` : toutes les informations, y compris l'éphéméride, l'heure estimée et la position. `eph` : éphéméride uniquement. `aid` : heure et position d'assistance. Par défaut : `full`. |
| **lat** | number | no | Latitude estimée de l'utilisateur, en degrés (-90 à 90). Les données de position d'assistance se présentent sous deux formats — lat/lon/alt ou ECEF — et vous en choisissez un. Le format lat/lon/alt exige les trois champs : `lat=30;lon=120.3;alt=100;` |
| **lon** | number | no | Longitude estimée de l'utilisateur, en degrés (-180 à 180). |
| **alt** | number | no | Altitude estimée de l'utilisateur, en mètres. |
| **x** | number | no | Coordonnée ECEF X estimée de l'utilisateur, en mètres. Le format ECEF exige les trois champs : `x=30000;y=1111120.3;z=3345100;` |
| **y** | number | no | Coordonnée ECEF Y estimée de l'utilisateur, en mètres. |
| **z** | number | no | Coordonnée ECEF Z estimée de l'utilisateur, en mètres. |
| **pacc** | number | no | Précision de la position de l'utilisateur, en mètres. |

2.5 **Réponse du serveur**

![réponse](../../en/09-raspberry-pi-agnss/images/2.png)

- Le serveur renvoie un en-tête de données suivi des données d'assistance.
- La charge utile binaire correspond aux données d'assistance dont le récepteur a besoin et comporte son propre checksum. Pour le format binaire, voir la spécification du protocole du récepteur CASIC.
- Transmettre également l'en-tête au récepteur est sans conséquence.

2.6 **Performance**

Comparé à un récepteur GNSS autonome, un récepteur AGNSS améliore nettement le TTFF, en particulier dans des conditions de signal faible.

![comparaison TTFF](../../en/09-raspberry-pi-agnss/images/3.jpg)

2.7 **Remarques**

- La position approximative doit être obtenue d'une autre manière, par exemple à partir de :
  - un module GSM/GPRS/3G, qui peut dériver une position approximative à partir de l'ID de cellule
  - le Wi-Fi ou un autre module sans fil, qui peut également localiser approximativement
- La position approximative doit être exacte à 15 km près ; une indication de position erronée dégrade les performances du récepteur.
- Si aucune position approximative n'est disponible, omettez les champs de position (lat, lon, alt, x, y, z) de la requête — le récepteur se rabat alors sur son dernier fix valide.
- Il n'est pas nécessaire d'utiliser la sortie du récepteur lui-même comme position approximative.

2.8 **Quand l'AGNSS est nécessaire**

Il n'est pas nécessaire de télécharger depuis le serveur à chaque démarrage, ce qui économise de la bande passante :

- Les puces CASIC disposent d'une SRAM sauvegardée par pile et d'une mémoire flash de secours permanente qui conservent les données d'éphéméride reçues.
- En fonctionnement normal, la puce continue de télécharger les dernières éphémérides depuis les satellites.
- Vous pouvez interroger l'état du récepteur pour décider si un téléchargement est nécessaire. Le récepteur peut émettre une trame d'état du message de navigation (désactivée par défaut ; elle doit être configurée).

2.9 **La trame d'état du message de navigation**

![trame 1](../../en/09-raspberry-pi-agnss/images/4.png)

![trame 2](../../en/09-raspberry-pi-agnss/images/5.png)

- Cette trame indique l'heure interne du récepteur et l'état du message de navigation.
- Envoyez `$PCAS03,,,,,,,,,,,1*1F` pour l'émettre une fois par seconde.
- Envoyez `$PCAS03,,,,,,,,,,,0*1E` pour cesser de l'émettre.
- Remarque : chaque trame doit se terminer par `\r\n` (0x0D, 0x0A) et contient 11 virgules.
- Si l'indicateur de temps est valide (non nul) et que le nombre d'éphémérides valides est élevé (plus de 8), il n'est pas nécessaire de télécharger les éphémérides AGNSS.

**3. Préparation**

**3.1 Câblage**

Le module GPS prend en charge la communication UART ou USB ; ici, nous utilisons l'USB.

![câblage](../../en/09-raspberry-pi-agnss/images/6.png)

Reliez le Raspberry Pi au module GPS avec un câble Type-C, puis exécutez `ls /dev | grep 'ttyUSB'` — le module est détecté sous `USB0`.

![détection du périphérique](../../en/09-raspberry-pi-agnss/images/7.png)

**3.2 Obtenir une clé AK Baidu Maps**

Voir [Demander une clé d'API Baidu Maps](baidu-map-api-key.md).

**4. Programme**

Le programme de cette leçon est `GPS-agnss.py`.

Initialisez l'USB :

![code](../../en/09-raspberry-pi-agnss/images/8.jpg)

Renseignez l'AK que vous avez demandée ; la latitude et la longitude approximatives actuelles peuvent alors être lues depuis Baidu Maps.

![code](../../en/09-raspberry-pi-agnss/images/9.jpg)

Les coordonnées approximatives issues de Baidu Maps sont envoyées au serveur — utilisez votre propre compte AGNSS — et une fois la procédure terminée, le paquet complet est envoyé au module.

![code](../../en/09-raspberry-pi-agnss/images/10.jpg)

![code](../../en/09-raspberry-pi-agnss/images/11.jpg)

La fonction d'acquisition et d'analyse de position filtre les données entrantes pour les trames commençant par `GNGGA` et les analyse dans des variables globales.

![code](../../en/09-raspberry-pi-agnss/images/12.jpg)

![code](../../en/09-raspberry-pi-agnss/images/13.jpg)

La même approche lit et analyse les informations de cap à partir de `GNVTG`.

![code](../../en/09-raspberry-pi-agnss/images/14.jpg)

Les données analysées sont affichées en boucle.

![code](../../en/09-raspberry-pi-agnss/images/15.jpg)

**5. Exécution du programme**

Exécutez `sudo python2 GPS-agnss.py` dans un terminal.

**6. Résultat**

**Remarque : avec le positionnement assisté, le Raspberry Pi doit avoir accès au réseau.**

Après la mise sous tension dans un environnement à signal faible, le programme initialise l'USB et affiche `GPS Serial Opened! Baudrate=9600` en cas de succès, ou `GPS Serial Open Failed!` en cas d'échec — en cas d'échec, vérifiez le câblage ou le port USB.

Il affiche ensuite `GPS Agnss start` pendant l'envoi des données d'assistance au serveur, et `GPS Agnss success` une fois terminé.

Tant qu'aucun signal GPS n'est acquis, il affiche `GPS no found` ainsi que les coordonnées approximatives lues depuis Baidu Maps.

![sortie](../../en/09-raspberry-pi-agnss/images/16.jpg)

Une fois le signal acquis, il affiche les informations de position et de cap en boucle.

![sortie](../../en/09-raspberry-pi-agnss/images/17.jpg)

Appuyez sur Ctrl+C pour arrêter la lecture.

![sortie](../../en/09-raspberry-pi-agnss/images/18.jpg)
