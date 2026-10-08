[English](README.md) | 简体中文

# GPS / 北斗定位模块

基于 **ATGM336H-5N** 的高性能 BDS/GNSS 定位导航模块。可同时接收北斗二号、北斗三号、GPS、GLONASS、QZSS 卫星信号并实现联合定位、导航与授时——高灵敏度、低功耗、低成本。

本仓库汇集了该模块的文档资料、接线说明，以及各平台的即用示例代码，均提供中英双语版本。

## 📦 仓库结构

| 路径 | 内容 |
|------|------|
| `docs/` | 模块介绍与[数据手册](docs/datasheets)（ATGM336H-5N 数据手册与用户手册、CASIC 协议规范） |
| `examples/51 microcontroller/` | STC89C52RC 例程：解析 NMEA 数据并通过串口打印位置信息 |
| `examples/arduino/` | Arduino UNO 例程：[读取位置信息](examples/arduino/position-read) 与 [解析位置信息](examples/arduino/position-parse) |
| `examples/stm32f103/` | STM32F103C8T6 例程：解析并输出位置信息，含度分转换 |
| `examples/jetson-nano/` | Jetson 例程：读取并解析位置信息，以及弱信号环境下的 [AGNSS 辅助定位](examples/jetson-nano/agnss) |
| `examples/raspberry-pi/` | 树莓派例程：与上面两篇教程相同 |
| `examples/ros/` | ROS 2 教程（编译、读数据、绘制轨迹、融合 IMU+GPS、GPS 与 Nav2）及[功能包源码](examples/ros/packages) |
| `tools/pc-gnss-toolkit/` | Windows 上位机工具，用于验证模块工作状态 |
| `troubleshooting/` | [地图定位误差](troubleshooting/map-position-error)：为什么在高德/百度地图上坐标会偏移，以及如何转换 |

每篇教程都有中英两个版本并互相跳转——`*.md` 是英文，`*_CN.md` 是简体中文。

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

完整参数见 [docs/overview_CN.md](docs/overview_CN.md)。

## 📄 许可

Copyright © 2026 Juxi Technology，**保留所有权利**——见 [LICENSE](LICENSE)。示例代码可用于评估和使用本模块；复制或再分发需获得书面许可。

厂商提供的资料（ATGM336H-5N 数据手册与用户手册、CASIC 协议规范、GnssToolKit3 上位机工具）版权归各自权利人所有，此处仅供查阅参考。
