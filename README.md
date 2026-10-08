English | [简体中文](README_CN.md)

# GPS / BeiDou Positioning Module

A high-performance BDS/GNSS positioning and navigation module built on the **ATGM336H-5N**. It receives BeiDou-2, BeiDou-3, GPS, GLONASS and QZSS simultaneously for combined positioning, navigation and timing — high sensitivity, low power, low cost.

This repository collects the module documentation, wiring notes and ready-to-run sample code for each supported platform, in both English and Simplified Chinese.

## 📦 Repository layout

| Path | Contents |
|------|----------|
| `docs/` | Module overview and the [datasheets](docs/datasheets) (ATGM336H-5N datasheet and user manual, CASIC protocol specification) |
| `examples/51 microcontroller/` | STC89C52RC example: parse the NMEA stream and print position data over UART |
| `examples/arduino/` | Arduino UNO examples: [reading position data](examples/arduino/position-read) and [parsing it](examples/arduino/position-parse) |
| `examples/stm32f103/` | STM32F103C8T6 example: parse and output position data, including the degrees-minutes conversion |
| `examples/jetson-nano/` | Jetson example: read and parse position data, plus [AGNSS-assisted positioning](examples/jetson-nano/agnss) for weak-signal environments |
| `examples/raspberry-pi/` | Raspberry Pi examples: same two tutorials as above |
| `examples/ros/` | ROS 2 tutorials (build, read data, plot a track, fuse IMU + GPS, GPS + Nav2) and the [package source](examples/ros/packages) |
| `tools/pc-gnss-toolkit/` | Windows host tool for verifying the module |
| `troubleshooting/` | [Map positioning error](troubleshooting/map-position-error): why coordinates are offset on Amap / Baidu Maps, and how to convert them |

Every tutorial exists in two versions and they link to each other — `*.md` is English, `*_CN.md` is Simplified Chinese.

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

See [docs/overview.md](docs/overview.md) for the full list.

## 📄 License

Copyright © 2026 Juxi Technology. **All rights reserved** — see [LICENSE](LICENSE). You may use the sample code to evaluate and operate the module; reproduction or redistribution requires written permission.

Vendor-supplied material (the ATGM336H-5N datasheets, the CASIC protocol specification and the GnssToolKit3 host tool) remains the property of its respective owners and is included for reference only.
