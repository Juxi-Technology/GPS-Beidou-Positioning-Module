[English](../../en/02-51-microcontroller/gps-data-parsing.md) | [Deutsch](../../de/02-51-microcontroller/gps-data-parsing.md) | [Español](../../es/02-51-microcontroller/gps-data-parsing.md) | [Français](../../fr/02-51-microcontroller/gps-data-parsing.md) | [Italiano](../../it/02-51-microcontroller/gps-data-parsing.md) | [日本語](../../ja/02-51-microcontroller/gps-data-parsing.md) | 한국어 | [Português (BR)](../../pt-br/02-51-microcontroller/gps-data-parsing.md) | [Português (PT)](../../pt-pt/02-51-microcontroller/gps-data-parsing.md) | [简体中文](../../zh-hans/02-51-microcontroller/gps-data-parsing.md) | [繁體中文](../../zh-hant/02-51-microcontroller/gps-data-parsing.md)

**GPS 데이터 파싱**

**1. 목표**

이번 장에서는 STC89C52RC(8051) 마이크로컨트롤러와 GPS 모듈을 함께 사용하여 위치 정보를 파싱합니다.

**2. 준비**

GPS 모듈은 UART와 USB를 통해 통신합니다. 여기에서는 8051의 UART로 데이터를 읽습니다. 모듈의 TX를 8051 보드의 P3.0 핀에, VCC와 GND를 5 V와 GND에 연결합니다.

![배선](../../en/02-51-microcontroller/images/1.png)

**3. 프로그램**

시리얼 포트와 데이터 배열을 초기화합니다.

![코드](../../en/02-51-microcontroller/images/2.jpg)

수신한 데이터를 읽고 파싱합니다.

![코드](../../en/02-51-microcontroller/images/3.jpg)

수신한 데이터를 시리얼 포트로 출력합니다.

![코드](../../en/02-51-microcontroller/images/4.jpg)

**4. 결과**

전원을 켜면 모듈이 시작되는 데 약 32초가 걸립니다. 그 이후에는 시리얼 상태 LED가 계속 깜빡이며 데이터를 정상적으로 수신할 수 있습니다.

프로그램을 다운로드하여 실행하고 9600 보드레이트로 시리얼 터미널을 열면 현재 위치 정보가 반복 출력됩니다.

![시리얼 출력](../../en/02-51-microcontroller/images/5.jpg)

모듈의 안테나는 반드시 실외에 두어야 하며, 그렇지 않으면 GPS 신호를 포착하지 못할 수 있습니다.
