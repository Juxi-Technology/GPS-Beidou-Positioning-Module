[English](../../en/10-ros-preparation/01-preparation.md) | [Deutsch](../../de/10-ros-preparation/01-preparation.md) | [Español](../../es/10-ros-preparation/01-preparation.md) | [Français](../../fr/10-ros-preparation/01-preparation.md) | [Italiano](../../it/10-ros-preparation/01-preparation.md) | [日本語](../../ja/10-ros-preparation/01-preparation.md) | [한국어](../../ko/10-ros-preparation/01-preparation.md) | [Português (BR)](../../pt-br/10-ros-preparation/01-preparation.md) | [Português (PT)](../../pt-pt/10-ros-preparation/01-preparation.md) | [简体中文](../../zh-hans/10-ros-preparation/01-preparation.md) | 繁體中文

### GPS模組使用前說明

#### 1、GPS模組編譯說明

（1）建立好工作空間後，把資料夾gps_src資料夾裡的內容複製到工作空間的src裡邊，然後利用colcon build編譯，沒有出現錯誤表示編譯通過；

在~/gps_ros2目錄下執行

```
colcon build
```

在~/gps_ros2目錄下執行 

```
source install/setup.bash
```

（2）功能套件內容說明：

- nmea_navsat_driver：GPS模組啟動、讀取GPS模組資料、繪製GPS資料等功能；
- nmea_msgs：存放一些GPS訊息的msg檔案
- imu_gps_localization：IMU與GPS資料融合功能
- gps_goal：轉換經緯度資料成Nav2目標導航資料

#### 2、綁定GPS連接埠

GPS模組透過序列埠與電腦或者主控連接，因此我們需要給GPS綁定好連接埠，以免連接埠號的問題導致GPS模組不能被電腦或者主控辨識出來。

（1）查看連接的USB裝置，找到GPS模組，終端機輸入**lsusb**查找GPS連接的裝置ID號，如下圖所示，就是GPS模組的裝置辨識ID，

![img_20260611114041](../../en/10-ros-preparation/images/1.png)

（2）知道了裝置號ID，那麼接下來就編寫rules檔案，綁定好連接埠，終端機輸入，

```
sudo gedit /etc/udev/rules.d/my_serial.rules 
```

把以下內容複製到裡邊，

```
KERNEL=="ttyUSB*", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", MODE:="0777", SYMLINK+="myserial"
```

儲存後離開，然後給它執行權限，終端機輸入，

```
sudo chmod 777 /etc/udev/rules.d/my_serial.rules 
```

（3）重新拔插GPS模組，終端機輸入ll /dev/myserial檢查是否綁定成功，出現以下畫面則表示成功綁定，

```
ll /dev/myserial
```

![img_20260611114128](../../en/10-ros-preparation/images/2.png)
