[English](01-preparation.md) | 简体中文

### GPS模块使用前说明

#### 1、GPS模块编译说明

（1）建立好工作空间后，把文件夹gps_src文件夹里的内容复制到工作空间的src里边，然后利用colcon build编译，没有出现错误表示编译通过；

在~/gps_ros2目录下运行

```
colcon build
```

在~/gps_ros2目录下运行 

```
source install/setup.bash
```

（2）功能包内容说明：

- nmea_navsat_driver：GPS模块启动、读取GPS模块数据、绘制GPS数据等功能；
- nmea_msgs：存放一些GPS消息的msg文件
- imu_gps_localization：IMU与GPS数据融合功能
- gps_goal：转换经纬度数据成Nav2目标导航数据

#### 2、绑定GPS端口

GPS模块通过串口与电脑或者主控连接，因此我们需要给GPS绑定好端口，以免端口号的问题导致GPS模块不能被电脑或者主控识别出来。

（1）查看连接的USB设备，找到GPS模块，终端输入**lsusb**查找GPS连接的设备ID号，如下图所示，就是GPS模块的设备识别ID，

![img_20260611114041](1.png)

（2）知道了设备号ID，那么接下来就编写rules文件，绑定好端口，终端输入，

```
sudo gedit /etc/udev/rules.d/my_serial.rules 
```

把以下内容复制到里边，

```
KERNEL=="ttyUSB*", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", MODE:="0777", SYMLINK+="myserial"
```

保存后退出，然后给它执行权限，终端输入，

```
sudo chmod 777 /etc/udev/rules.d/my_serial.rules 
```

（3）重新拔插GPS模块，终端输入ll /dev/myserial检查是否绑定成功，出现以下画面则表示成功绑定，

```
ll /dev/myserial
```

![img_20260611114128](2.png)
