English | [Deutsch](../../de/10-ros-preparation/01-preparation.md) | [Español](../../es/10-ros-preparation/01-preparation.md) | [Français](../../fr/10-ros-preparation/01-preparation.md) | [Italiano](../../it/10-ros-preparation/01-preparation.md) | [日本語](../../ja/10-ros-preparation/01-preparation.md) | [한국어](../../ko/10-ros-preparation/01-preparation.md) | [Português (BR)](../../pt-br/10-ros-preparation/01-preparation.md) | [Português (PT)](../../pt-pt/10-ros-preparation/01-preparation.md) | [简体中文](../../zh-hans/10-ros-preparation/01-preparation.md) | [繁體中文](../../zh-hant/10-ros-preparation/01-preparation.md)

### Before You Start

#### 1. Building the GPS packages

(1) Create a workspace, copy the contents of the `gps_src` folder into the workspace's `src` directory, then build with `colcon build`. If no errors appear, the build succeeded.

In `~/gps_ros2`:

```
colcon build
```

Then in `~/gps_ros2`:

```
source install/setup.bash
```

(2) What each package contains:

- `nmea_navsat_driver` — starting the GPS module, reading its data, and drawing GPS tracks
- `nmea_msgs` — message definitions for GPS-related messages
- `imu_gps_localization` — fusing IMU and GPS data
- `gps_goal` — converting latitude/longitude into a Nav2 goal

#### 2. Binding a fixed port to the GPS module

The GPS module talks to the PC or host over a serial port, so we bind a fixed port name to it — otherwise a changing port number can stop the host from finding the module.

(1) List the connected USB devices and locate the GPS module. Run **lsusb** and note the device ID, as shown below.

![lsusb output](images/1.png)

(2) With the device ID known, write a udev rules file to bind the port. Run:

```
sudo gedit /etc/udev/rules.d/my_serial.rules
```

and paste in the following:

```
KERNEL=="ttyUSB*", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", MODE:="0777", SYMLINK+="myserial"
```

Save, exit, then make it executable:

```
sudo chmod 777 /etc/udev/rules.d/my_serial.rules
```

(3) Unplug and replug the GPS module, then run `ll /dev/myserial` to check that the binding worked. The output below means it succeeded.

```
ll /dev/myserial
```

![udev binding](images/2.png)
