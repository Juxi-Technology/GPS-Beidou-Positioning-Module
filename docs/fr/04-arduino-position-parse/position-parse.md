[English](../../en/04-arduino-position-parse/position-parse.md) | [Deutsch](../../de/04-arduino-position-parse/position-parse.md) | [Español](../../es/04-arduino-position-parse/position-parse.md) | Français | [Italiano](../../it/04-arduino-position-parse/position-parse.md) | [日本語](../../ja/04-arduino-position-parse/position-parse.md) | [한국어](../../ko/04-arduino-position-parse/position-parse.md) | [Português (BR)](../../pt-br/04-arduino-position-parse/position-parse.md) | [Português (PT)](../../pt-pt/04-arduino-position-parse/position-parse.md) | [简体中文](../../zh-hans/04-arduino-position-parse/position-parse.md) | [繁體中文](../../zh-hant/04-arduino-position-parse/position-parse.md)

**Analyse des données de position GPS**

**1. Objectifs**

Dans cette leçon, nous utilisons un Arduino et le module GPS pour analyser et afficher les informations de position.

**2. Préparation**

Le module GPS communique via UART et USB. Ici, nous utilisons l'UART de l'Arduino UNO : reliez le TX du module à la broche D0 de l'UNO, et le VCC et le GND à 5 V et GND.

![câblage](../../en/04-arduino-position-parse/images/1.png)

**3. Programme**

Initialisez le port série.

![code](../../en/04-arduino-position-parse/images/2.jpg)

Lisez les données série.

![code](../../en/04-arduino-position-parse/images/3.jpg)

Analysez les données série.

![code](../../en/04-arduino-position-parse/images/4.jpg)

Affichez les informations de position analysées.

![code](../../en/04-arduino-position-parse/images/5.jpg)

**4. Compilation et téléversement**

4.1 Ouvrez le fichier dans l'IDE Arduino, cliquez sur le bouton « ✓ » pour compiler, et attendez « Done compiling ».

![compilation](../../en/04-arduino-position-parse/images/6.jpg)

4.2 Dans le menu, sélectionnez Tools → Port → le port affiché dans le Gestionnaire de périphériques.

![sélection du port](../../en/04-arduino-position-parse/images/7.jpg)

4.3 Cliquez sur le bouton « → » pour téléverser. Lorsque « Done uploading » apparaît, le téléversement a réussi.

![téléversement](../../en/04-arduino-position-parse/images/8.jpg)

**5. Résultat**

Après la mise sous tension, le module a besoin d'environ 32 s pour démarrer ; ensuite, la LED d'état série clignote en continu et les données peuvent être reçues normalement.

Exécutez le programme, ouvrez le moniteur série à 9600 bauds, et les informations de position en temps réel analysées sont affichées en boucle.

![sortie série](../../en/04-arduino-position-parse/images/9.jpg)

Notez que l'antenne du module doit être à l'extérieur, sinon il risque de ne pas capter de signal GPS.
