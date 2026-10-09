[English](../../en/10-ros-preparation/01-preparation.md) | [Deutsch](../../de/10-ros-preparation/01-preparation.md) | [Español](../../es/10-ros-preparation/01-preparation.md) | Français | [Italiano](../../it/10-ros-preparation/01-preparation.md) | [日本語](../../ja/10-ros-preparation/01-preparation.md) | [한국어](../../ko/10-ros-preparation/01-preparation.md) | [Português (BR)](../../pt-br/10-ros-preparation/01-preparation.md) | [Português (PT)](../../pt-pt/10-ros-preparation/01-preparation.md) | [简体中文](../../zh-hans/10-ros-preparation/01-preparation.md) | [繁體中文](../../zh-hant/10-ros-preparation/01-preparation.md)

### Avant de commencer

#### 1. Compilation des paquets GPS

(1) Créez un espace de travail, copiez le contenu du dossier `gps_src` dans le répertoire `src` de l'espace de travail, puis compilez avec `colcon build`. Si aucune erreur n'apparaît, la compilation a réussi.

Dans `~/gps_ros2` :

```
colcon build
```

Puis dans `~/gps_ros2` :

```
source install/setup.bash
```

(2) Contenu de chaque paquet :

- `nmea_navsat_driver` — démarrage du module GPS, lecture de ses données et tracé des trajectoires GPS
- `nmea_msgs` — définitions des messages liés au GPS
- `imu_gps_localization` — fusion des données IMU et GPS
- `gps_goal` — conversion de la latitude/longitude en objectif Nav2

#### 2. Lier un port fixe au module GPS

Le module GPS communique avec le PC ou l'hôte via un port série ; nous lui associons donc un nom de port fixe — sinon, un numéro de port changeant peut empêcher l'hôte de trouver le module.

(1) Listez les périphériques USB connectés et repérez le module GPS. Exécutez **lsusb** et notez l'ID du périphérique, comme ci-dessous.

![sortie lsusb](../../en/10-ros-preparation/images/1.png)

(2) Une fois l'ID du périphérique connu, écrivez un fichier de règles udev pour lier le port. Exécutez :

```
sudo gedit /etc/udev/rules.d/my_serial.rules
```

et collez ce qui suit :

```
KERNEL=="ttyUSB*", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", MODE:="0777", SYMLINK+="myserial"
```

Enregistrez, quittez, puis rendez-le exécutable :

```
sudo chmod 777 /etc/udev/rules.d/my_serial.rules
```

(3) Débranchez puis rebranchez le module GPS, puis exécutez `ll /dev/myserial` pour vérifier que la liaison a fonctionné. La sortie ci-dessous signifie que cela a réussi.

```
ll /dev/myserial
```

![liaison udev](../../en/10-ros-preparation/images/2.png)
