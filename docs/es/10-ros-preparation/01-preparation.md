[English](../../en/10-ros-preparation/01-preparation.md) | [Deutsch](../../de/10-ros-preparation/01-preparation.md) | Español | [Français](../../fr/10-ros-preparation/01-preparation.md) | [Italiano](../../it/10-ros-preparation/01-preparation.md) | [日本語](../../ja/10-ros-preparation/01-preparation.md) | [한국어](../../ko/10-ros-preparation/01-preparation.md) | [Português (BR)](../../pt-br/10-ros-preparation/01-preparation.md) | [Português (PT)](../../pt-pt/10-ros-preparation/01-preparation.md) | [简体中文](../../zh-hans/10-ros-preparation/01-preparation.md) | [繁體中文](../../zh-hant/10-ros-preparation/01-preparation.md)

### Antes de empezar

#### 1. Compilación de los paquetes GPS

(1) Crea un espacio de trabajo, copia el contenido de la carpeta `gps_src` en el directorio `src` del espacio de trabajo y compílalo con `colcon build`. Si no aparece ningún error, la compilación se ha realizado correctamente.

En `~/gps_ros2`:

```
colcon build
```

Después, en `~/gps_ros2`:

```
source install/setup.bash
```

(2) Contenido de cada paquete:

- `nmea_navsat_driver`: inicia el módulo GPS, lee sus datos y dibuja trayectorias GPS
- `nmea_msgs`: definiciones de los mensajes relacionados con GPS
- `imu_gps_localization`: fusiona datos de IMU y GPS
- `gps_goal`: convierte latitud/longitud en un objetivo de Nav2

#### 2. Vincular un puerto fijo al módulo GPS

El módulo GPS se comunica con el PC o el host a través de un puerto serie, por lo que le vinculamos un nombre de puerto fijo; de lo contrario, un número de puerto cambiante puede impedir que el host encuentre el módulo.

(1) Enumera los dispositivos USB conectados y localiza el módulo GPS. Ejecuta **lsusb** y anota el ID del dispositivo, como se muestra a continuación.

![salida de lsusb](../../en/10-ros-preparation/images/1.png)

(2) Una vez conocido el ID del dispositivo, escribe un archivo de reglas udev para vincular el puerto. Ejecuta:

```
sudo gedit /etc/udev/rules.d/my_serial.rules
```

y pega lo siguiente:

```
KERNEL=="ttyUSB*", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", MODE:="0777", SYMLINK+="myserial"
```

Guarda, sal y hazlo ejecutable:

```
sudo chmod 777 /etc/udev/rules.d/my_serial.rules
```

(3) Desconecta y vuelve a conectar el módulo GPS, luego ejecuta `ll /dev/myserial` para comprobar que la vinculación ha funcionado. La salida de abajo indica que se ha realizado correctamente.

```
ll /dev/myserial
```

![vinculación udev](../../en/10-ros-preparation/images/2.png)
