[English](../../en/10-ros-preparation/01-preparation.md) | [Deutsch](../../de/10-ros-preparation/01-preparation.md) | [Español](../../es/10-ros-preparation/01-preparation.md) | [Français](../../fr/10-ros-preparation/01-preparation.md) | Italiano | [日本語](../../ja/10-ros-preparation/01-preparation.md) | [한국어](../../ko/10-ros-preparation/01-preparation.md) | [Português (BR)](../../pt-br/10-ros-preparation/01-preparation.md) | [Português (PT)](../../pt-pt/10-ros-preparation/01-preparation.md) | [简体中文](../../zh-hans/10-ros-preparation/01-preparation.md) | [繁體中文](../../zh-hant/10-ros-preparation/01-preparation.md)

### Prima di iniziare

#### 1. Compilazione dei pacchetti GPS

(1) Creare un workspace, copiare il contenuto della cartella `gps_src` nella cartella `src` del workspace, quindi compilare con `colcon build`. Se non compaiono errori, la compilazione è riuscita.

In `~/gps_ros2`:

```
colcon build
```

Poi in `~/gps_ros2`:

```
source install/setup.bash
```

(2) Contenuto di ciascun pacchetto:

- `nmea_navsat_driver` — avvio del modulo GPS, lettura dei suoi dati e tracciatura dei percorsi GPS
- `nmea_msgs` — definizioni dei messaggi per i messaggi relativi al GPS
- `imu_gps_localization` — fusione dei dati IMU e GPS
- `gps_goal` — conversione di latitudine/longitudine in un goal di Nav2

#### 2. Associazione di una porta fissa al modulo GPS

Il modulo GPS comunica con il PC o l'host tramite una porta seriale, quindi gli si associa un nome di porta fisso — altrimenti un numero di porta variabile può impedire all'host di trovare il modulo.

(1) Elencare i dispositivi USB collegati e individuare il modulo GPS. Eseguire **lsusb** e annotare l'ID del dispositivo, come mostrato di seguito.

![output di lsusb](../../en/10-ros-preparation/images/1.png)

(2) Noto l'ID del dispositivo, scrivere un file di regole udev per associare la porta. Eseguire:

```
sudo gedit /etc/udev/rules.d/my_serial.rules
```

e incollare quanto segue:

```
KERNEL=="ttyUSB*", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", MODE:="0777", SYMLINK+="myserial"
```

Salvare, uscire, quindi renderlo eseguibile:

```
sudo chmod 777 /etc/udev/rules.d/my_serial.rules
```

(3) Scollegare e ricollegare il modulo GPS, quindi eseguire `ll /dev/myserial` per verificare che l'associazione abbia funzionato. L'output riportato di seguito indica che è riuscita.

```
ll /dev/myserial
```

![associazione udev](../../en/10-ros-preparation/images/2.png)
