English | [简体中文](README_CN.md)

# GPS / BeiDou Positioning Module

A high-performance BDS/GNSS positioning and navigation module built on the **ATGM336H-5N**. It receives BeiDou-2, BeiDou-3, GPS, GLONASS and QZSS simultaneously for combined positioning, navigation and timing — high sensitivity, low power, low cost.

This repository collects the module documentation, wiring notes and ready-to-run sample code for each supported platform, in 11 languages.

## 📦 Repository layout

| Path | Contents |
|------|----------|
| `docs/<lang>/` | Tutorials — the same 15-stage set in each language tree. Images are stored only under `docs/en/`; every other language links to them. |
| `docs/datasheets/` | Vendor documents: [ATGM336H-5N](docs/datasheets) datasheet and user manual, CASIC protocol specification |
| `examples/` | Source code per platform — `51 microcontroller/`, `arduino/`, `stm32f103/`, `jetson-nano/`, `raspberry-pi/`, `ros/` |
| `tools/pc-gnss-toolkit/` | Windows host tool for verifying the module |

| Language | Folder |
|----------|--------|
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

### Tutorials

| Stage | English | 简体中文 |
|-------|---------|----------|
| 01 Module overview | [overview](docs/en/01-overview/overview.md) | [概述](docs/zh-hans/01-overview/overview.md) |
| 02 51 microcontroller | [gps-data-parsing](docs/en/02-51-microcontroller/gps-data-parsing.md) | [GPS 数据解析](docs/zh-hans/02-51-microcontroller/gps-data-parsing.md) |
| 03 Arduino — reading | [position-read](docs/en/03-arduino-position-read/position-read.md) | [读取位置信息](docs/zh-hans/03-arduino-position-read/position-read.md) |
| 04 Arduino — parsing | [position-parse](docs/en/04-arduino-position-parse/position-parse.md) | [解析位置信息](docs/zh-hans/04-arduino-position-parse/position-parse.md) |
| 05 STM32F103 | [gps-parse-output](docs/en/05-stm32f103/gps-parse-output.md) | [GPS 解析输出](docs/zh-hans/05-stm32f103/gps-parse-output.md) |
| 06 Jetson — parsing | [position-parse](docs/en/06-jetson-nano-position-parse/position-parse.md) | [解析位置信息](docs/zh-hans/06-jetson-nano-position-parse/position-parse.md) |
| 07 Jetson — AGNSS | [agnss](docs/en/07-jetson-nano-agnss/agnss.md) · [Baidu key](docs/en/07-jetson-nano-agnss/baidu-map-api-key.md) | [AGNSS](docs/zh-hans/07-jetson-nano-agnss/agnss.md) · [百度 AK](docs/zh-hans/07-jetson-nano-agnss/baidu-map-api-key.md) |
| 08 Raspberry Pi — parsing | [position-parse](docs/en/08-raspberry-pi-position-parse/position-parse.md) | [解析位置信息](docs/zh-hans/08-raspberry-pi-position-parse/position-parse.md) |
| 09 Raspberry Pi — AGNSS | [agnss](docs/en/09-raspberry-pi-agnss/agnss.md) · [Baidu key](docs/en/09-raspberry-pi-agnss/baidu-map-api-key.md) | [AGNSS](docs/zh-hans/09-raspberry-pi-agnss/agnss.md) · [百度 AK](docs/zh-hans/09-raspberry-pi-agnss/baidu-map-api-key.md) |
| 10 ROS 2 — preparation | [01-preparation](docs/en/10-ros-preparation/01-preparation.md) | [使用前准备](docs/zh-hans/10-ros-preparation/01-preparation.md) |
| 11 ROS 2 — reading data | [02-read-gps-data](docs/en/11-ros-read-gps-data/02-read-gps-data.md) | [读取 GPS 数据](docs/zh-hans/11-ros-read-gps-data/02-read-gps-data.md) |
| 12 ROS 2 — plotting a track | [03-plot-gps-track](docs/en/12-ros-plot-gps-track/03-plot-gps-track.md) | [绘制 GPS 轨迹](docs/zh-hans/12-ros-plot-gps-track/03-plot-gps-track.md) |
| 13 ROS 2 — IMU + GPS fusion | [04-imu-gps-fusion](docs/en/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [融合 IMU 和 GPS](docs/zh-hans/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) |
| 14 ROS 2 — Nav2 | [05-gps-nav2](docs/en/14-ros-nav2/05-gps-nav2.md) | [GPS 与 Nav2](docs/zh-hans/14-ros-nav2/05-gps-nav2.md) |
| 15 Map positioning error | [map-position-error](docs/en/15-map-position-error/map-position-error.md) | [地图定位误差](docs/zh-hans/15-map-position-error/map-position-error.md) |

Every page carries a language switcher at the top — use it to move between the English and Chinese version of the same stage.

## 🔌 Quick start

1. Connect the module to your board over UART or USB — see each example's wiring note (`wiring.txt` where provided).
2. Power it and wait about 32 seconds for the first fix. The status LED blinks continuously once data is available.
3. Set the serial baud rate to **9600**.
4. Run the example for your platform.

Keep the antenna outdoors — the module may not acquire a fix indoors.

## 📐 Key specifications

| Parameter | Value |
|-----------|-------|
| Constellation support | BeiDou-2 / BeiDou-3 (IDs 1–63), GPS, GLONASS, QZSS |
| Cold-start acquisition sensitivity | -148 dBm |
| Tracking sensitivity | -162 dBm |
| Positioning accuracy | 2.5 m (CEP50) |
| Time to first fix | 32 s |
| Power consumption | 25 mA @ 3.3 V (continuous) |
| A-GNSS | Supported |

See [the module overview](docs/en/01-overview/overview.md) for the full list.

## 📄 License

Copyright © 2026 Juxi Technology. **All rights reserved** — see [LICENSE](LICENSE). You may use the sample code to evaluate and operate the module; reproduction or redistribution requires written permission.

Vendor-supplied material (the ATGM336H-5N datasheets, the CASIC protocol specification and the GnssToolKit3 host tool) remains the property of its respective owners and is included for reference only.
