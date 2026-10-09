[English](../../en/03-arduino-position-read/position-read.md) | [Deutsch](../../de/03-arduino-position-read/position-read.md) | [Español](../../es/03-arduino-position-read/position-read.md) | Français | [Italiano](../../it/03-arduino-position-read/position-read.md) | [日本語](../../ja/03-arduino-position-read/position-read.md) | [한국어](../../ko/03-arduino-position-read/position-read.md) | [Português (BR)](../../pt-br/03-arduino-position-read/position-read.md) | [Português (PT)](../../pt-pt/03-arduino-position-read/position-read.md) | [简体中文](../../zh-hans/03-arduino-position-read/position-read.md) | [繁體中文](../../zh-hant/03-arduino-position-read/position-read.md)

**Lecture des données de position GPS**

**1. Objectifs**

Dans cette leçon, nous utilisons un Arduino et le module GPS pour lire les informations de position.

**2. Préparation**

Le module GPS communique via UART et USB. Ici, nous utilisons l'UART de l'Arduino UNO : reliez le TX du module à la broche D0 de l'UNO, et le VCC et le GND à 5 V et GND.

![câblage](../../en/03-arduino-position-read/images/1.png)

**3. Programme**

Initialisez le port série.

![code](../../en/03-arduino-position-read/images/2.jpg)

Affichez les données reçues.

**4. Compilation et téléversement**

4.1 Ouvrez le fichier dans l'IDE Arduino, cliquez sur le bouton « ✓ » de la barre d'outils pour compiler, et attendez « Done compiling » dans la barre d'état.

![compilation](../../en/03-arduino-position-read/images/3.jpg)

4.2 Dans le menu de l'IDE Arduino, sélectionnez Tools → Port → le port affiché dans le Gestionnaire de périphériques, comme ci-dessous.

![sélection du port](../../en/03-arduino-position-read/images/4.jpg)

4.3 Cliquez ensuite sur le bouton « → » pour téléverser le code vers la carte UNO. Lorsque « Done uploading » apparaît, le téléversement a réussi.

![téléversement](../../en/03-arduino-position-read/images/5.jpg)

**5. Résultat**

Après la mise sous tension, le module a besoin d'environ 32 s pour démarrer ; ensuite, la LED d'état série clignote en continu et les données peuvent être reçues normalement.

Exécutez le programme, ouvrez le moniteur série et réglez le débit en bauds sur 9600. Les informations de position actuelles sont affichées en boucle. Il s'agit de données brutes, non traitées — voir la [spécification du protocole CASIC GNSS](../../../docs/datasheets/CASIC-GNSS-protocol-spec-CN.pdf) pour la signification de chaque trame.

![sortie série](../../en/03-arduino-position-read/images/6.jpg)

Notez que l'antenne du module doit être à l'extérieur, sinon il risque de ne pas capter de signal GPS.
