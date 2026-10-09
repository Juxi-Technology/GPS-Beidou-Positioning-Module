[English](README.md) | 简体中文

# GPS / 北斗定位模块

基于 **ATGM336H-5N** 的高性能 BDS/GNSS 定位导航模块。可同时接收北斗二号、北斗三号、GPS、GLONASS、QZSS 卫星信号并实现联合定位、导航与授时——高灵敏度、低功耗、低成本。

本仓库汇集了该模块的文档资料、接线说明，以及各平台的即用示例代码，均提供 11 种语言版本。

## 📦 仓库结构

| 路径 | 内容 |
|------|------|
| `docs/<语言>/` | 教程——各语言目录内容一一对应。**图片只存放在 `docs/en/` 下**，其他语言引用它们。 |
| `docs/datasheets/` | 厂商资料：[ATGM336H-5N](docs/datasheets) 数据手册与用户手册、CASIC 协议规范 |
| `examples/` | 各平台源码——`51 microcontroller/`、`arduino/`、`stm32f103/`、`jetson-nano/`、`raspberry-pi/`、`ros/` |
| `tools/pc-gnss-toolkit/` | Windows 上位机工具，用于验证模块工作状态 |

| 语言 | 目录 |
|------|------|
| English | [`docs/en/`](docs/en/) |
| Deutsch | [`docs/de/`](docs/de/) |
| Español | [`docs/es/`](docs/es/) |
| Français | [`docs/fr/`](docs/fr/) |
| Italiano | [`docs/it/`](docs/it/) |
| 日本語 | [`docs/ja/`](docs/ja/) |
| 한국어 | [`docs/ko/`](docs/ko/) |
| Português (BR) | [`docs/pt-br/`](docs/pt-br/) |
| Português (PT) | [`docs/pt-pt/`](docs/pt-pt/) |
| 简体中文 | [`docs/zh-hans/`](docs/zh-hans/) |
| 繁體中文 | [`docs/zh-hant/`](docs/zh-hant/) |

### 教程列表

| 阶段 | English | 简体中文 |
|------|---------|----------|
| 01 模块概述 | [overview](docs/en/01-overview/overview.md) | [概述](docs/zh-hans/01-overview/overview.md) |
| 02 51 单片机 | [gps-data-parsing](docs/en/02-51-microcontroller/gps-data-parsing.md) | [GPS 数据解析](docs/zh-hans/02-51-microcontroller/gps-data-parsing.md) |
| 03 Arduino 读取 | [position-read](docs/en/03-arduino-position-read/position-read.md) | [读取位置信息](docs/zh-hans/03-arduino-position-read/position-read.md) |
| 04 Arduino 解析 | [position-parse](docs/en/04-arduino-position-parse/position-parse.md) | [解析位置信息](docs/zh-hans/04-arduino-position-parse/position-parse.md) |
| 05 STM32F103 | [gps-parse-output](docs/en/05-stm32f103/gps-parse-output.md) | [GPS 解析输出](docs/zh-hans/05-stm32f103/gps-parse-output.md) |
| 06 Jetson 解析 | [position-parse](docs/en/06-jetson-nano-position-parse/position-parse.md) | [解析位置信息](docs/zh-hans/06-jetson-nano-position-parse/position-parse.md) |
| 07 Jetson AGNSS | [agnss](docs/en/07-jetson-nano-agnss/agnss.md) · [百度 AK](docs/en/07-jetson-nano-agnss/baidu-map-api-key.md) | [AGNSS](docs/zh-hans/07-jetson-nano-agnss/agnss.md) · [百度 AK](docs/zh-hans/07-jetson-nano-agnss/baidu-map-api-key.md) |
| 08 树莓派解析 | [position-parse](docs/en/08-raspberry-pi-position-parse/position-parse.md) | [解析位置信息](docs/zh-hans/08-raspberry-pi-position-parse/position-parse.md) |
| 09 树莓派 AGNSS | [agnss](docs/en/09-raspberry-pi-agnss/agnss.md) · [百度 AK](docs/en/09-raspberry-pi-agnss/baidu-map-api-key.md) | [AGNSS](docs/zh-hans/09-raspberry-pi-agnss/agnss.md) · [百度 AK](docs/zh-hans/09-raspberry-pi-agnss/baidu-map-api-key.md) |
| 10 ROS 2 使用前准备 | [01-preparation](docs/en/10-ros-preparation/01-preparation.md) | [使用前准备](docs/zh-hans/10-ros-preparation/01-preparation.md) |
| 11 ROS 2 读取数据 | [02-read-gps-data](docs/en/11-ros-read-gps-data/02-read-gps-data.md) | [读取 GPS 数据](docs/zh-hans/11-ros-read-gps-data/02-read-gps-data.md) |
| 12 ROS 2 绘制轨迹 | [03-plot-gps-track](docs/en/12-ros-plot-gps-track/03-plot-gps-track.md) | [绘制 GPS 轨迹](docs/zh-hans/12-ros-plot-gps-track/03-plot-gps-track.md) |
| 13 ROS 2 融合 IMU+GPS | [04-imu-gps-fusion](docs/en/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [融合 IMU 和 GPS](docs/zh-hans/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) |
| 14 ROS 2 与 Nav2 | [05-gps-nav2](docs/en/14-ros-nav2/05-gps-nav2.md) | [GPS 与 Nav2](docs/zh-hans/14-ros-nav2/05-gps-nav2.md) |
| 15 地图定位误差 | [map-position-error](docs/en/15-map-position-error/map-position-error.md) | [地图定位误差](docs/zh-hans/15-map-position-error/map-position-error.md) |

每篇文档顶部都有语言切换条，可在同一阶段的中英版本间跳转。

## 🔌 快速开始

1. 通过 UART 或 USB 将模块接到主控板——接线见各例程目录下的说明（部分提供了 `wiring.txt`）。
2. 上电后等待约 32 秒完成首次定位。数据可用时状态灯会持续闪烁。
3. 串口波特率设置为 **9600**。
4. 运行对应平台的例程。

天线需置于室外——在室内可能搜不到卫星信号。

## 📐 主要参数

| 参数 | 数值 |
|------|------|
| 支持星座 | 北斗二号 / 北斗三号（1~63 号）、GPS、GLONASS、QZSS |
| 冷启动捕获灵敏度 | -148 dBm |
| 跟踪灵敏度 | -162 dBm |
| 定位精度 | 2.5 米（CEP50） |
| 首次定位时间 | 32 秒 |
| 功耗 | 连续运行 25 mA @ 3.3 V |
| A-GNSS | 支持 |

完整参数见[模块概述](docs/zh-hans/01-overview/overview.md)。

## 📄 许可

Copyright © 2026 Juxi Technology，**保留所有权利**——见 [LICENSE](LICENSE)。示例代码可用于评估和使用本模块；复制或再分发需获得书面许可。

厂商提供的资料（ATGM336H-5N 数据手册与用户手册、CASIC 协议规范、GnssToolKit3 上位机工具）版权归各自权利人所有，此处仅供查阅参考。
