[English](../../en/02-51-microcontroller/gps-data-parsing.md) | [Deutsch](../../de/02-51-microcontroller/gps-data-parsing.md) | [Español](../../es/02-51-microcontroller/gps-data-parsing.md) | Français | [Italiano](../../it/02-51-microcontroller/gps-data-parsing.md) | [日本語](../../ja/02-51-microcontroller/gps-data-parsing.md) | [한국어](../../ko/02-51-microcontroller/gps-data-parsing.md) | [Português (BR)](../../pt-br/02-51-microcontroller/gps-data-parsing.md) | [Português (PT)](../../pt-pt/02-51-microcontroller/gps-data-parsing.md) | [简体中文](../../zh-hans/02-51-microcontroller/gps-data-parsing.md) | [繁體中文](../../zh-hant/02-51-microcontroller/gps-data-parsing.md)

**Analyse des données GPS**

**1. Objectifs**

Dans cette leçon, nous utilisons un microcontrôleur STC89C52RC (8051) avec le module GPS pour analyser les informations de position.

**2. Préparation**

Le module GPS communique via UART et USB. Ici, nous le lisons via l'UART du 8051 : reliez le TX du module à la broche P3.0 de la carte 8051, et le VCC et le GND à 5 V et GND.

![câblage](../../en/02-51-microcontroller/images/1.png)

**3. Programme**

Initialisez le port série et le tableau de données.

![code](../../en/02-51-microcontroller/images/2.jpg)

Lisez et analysez les données entrantes.

![code](../../en/02-51-microcontroller/images/3.jpg)

Affichez les données reçues via le port série.

![code](../../en/02-51-microcontroller/images/4.jpg)

**4. Résultat**

Après la mise sous tension, le module a besoin d'environ 32 s pour démarrer ; ensuite, la LED d'état série clignote en continu et les données peuvent être reçues normalement.

Téléchargez et exécutez le programme, ouvrez un terminal série à 9600 bauds, et les informations de position actuelles sont affichées en boucle.

![sortie série](../../en/02-51-microcontroller/images/5.jpg)

Notez que l'antenne du module doit être à l'extérieur, sinon il risque de ne pas capter de signal GPS.
