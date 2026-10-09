[English](../../en/05-stm32f103/gps-parse-output.md) | [Deutsch](../../de/05-stm32f103/gps-parse-output.md) | [Español](../../es/05-stm32f103/gps-parse-output.md) | Français | [Italiano](../../it/05-stm32f103/gps-parse-output.md) | [日本語](../../ja/05-stm32f103/gps-parse-output.md) | [한국어](../../ko/05-stm32f103/gps-parse-output.md) | [Português (BR)](../../pt-br/05-stm32f103/gps-parse-output.md) | [Português (PT)](../../pt-pt/05-stm32f103/gps-parse-output.md) | [简体中文](../../zh-hans/05-stm32f103/gps-parse-output.md) | [繁體中文](../../zh-hant/05-stm32f103/gps-parse-output.md)

**Analyse et sortie des données GPS (STM32)**

**1. Objectifs**

Dans cette leçon, nous utilisons un STM32F103C8T6 et le module GPS pour analyser et produire les informations de position.

**2. Préparation**

Le module GPS communique via UART et USB. Ici, nous utilisons l'UART du STM32 : reliez le TXD du module à la broche PA10 de la carte STM32F103C8T6, et le VCC et le GND au 5 V et GND de la carte. Reliez le GND et le RXD de l'adaptateur TTL au GND et au PA9 du STM32.

![câblage](../../en/05-stm32f103/images/1.png)

**3. Programme**

Le débit en bauds du module est 9600.

![code](../../en/05-stm32f103/images/2.jpg)

Lisez et analysez les données entrantes.

![code](../../en/05-stm32f103/images/3.jpg)

Convertissez les unités de latitude / longitude en degrés.

![code](../../en/05-stm32f103/images/4.jpg)

Affichez les données reçues via le port série.

![code](../../en/05-stm32f103/images/5.jpg)

Note : la latitude et la longitude issues du GPS / BeiDou ne suivent pas une simple relation ×100 — elles nécessitent une conversion degrés-minutes. Par exemple, pour une latitude `2429.53531` N et une longitude `11810.78036` E :

```
24 + (29.53531 / 60) ≈ 24.49225517
118 + (10.78036 / 60) ≈ 118.17967267
```

Les différents microcontrôleurs peuvent aussi introduire une petite erreur en raison de la précision de conversion des données.

**4. Résultat**

Après la mise sous tension, le module a besoin d'environ 32 s pour démarrer ; ensuite, la LED d'état série clignote en continu et les données peuvent être reçues normalement.

Téléchargez et exécutez le programme, ouvrez un terminal série à 9600 bauds, et les informations de position actuelles sont affichées en boucle.

![sortie série](../../en/05-stm32f103/images/6.jpg)

Notez que l'antenne du module doit être à l'extérieur, sinon il risque de ne pas capter de signal GPS.
