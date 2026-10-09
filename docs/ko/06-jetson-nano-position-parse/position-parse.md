[English](../../en/06-jetson-nano-position-parse/position-parse.md) | [Deutsch](../../de/06-jetson-nano-position-parse/position-parse.md) | [Español](../../es/06-jetson-nano-position-parse/position-parse.md) | [Français](../../fr/06-jetson-nano-position-parse/position-parse.md) | [Italiano](../../it/06-jetson-nano-position-parse/position-parse.md) | [日本語](../../ja/06-jetson-nano-position-parse/position-parse.md) | 한국어 | [Português (BR)](../../pt-br/06-jetson-nano-position-parse/position-parse.md) | [Português (PT)](../../pt-pt/06-jetson-nano-position-parse/position-parse.md) | [简体中文](../../zh-hans/06-jetson-nano-position-parse/position-parse.md) | [繁體中文](../../zh-hant/06-jetson-nano-position-parse/position-parse.md)

**GPS 위치 데이터 읽기 및 파싱 (Jetson)**

**1. 목표**

이번 장에서는 Jetson Orin과 GPS 모듈을 사용하여 위치 정보를 읽고 파싱합니다.

**2. 준비**

GPS 모듈은 UART 또는 USB 통신을 지원하며, 여기에서는 USB를 사용합니다.

![모듈](../../en/06-jetson-nano-position-parse/images/1.png)

Type-C 케이블로 Jetson Orin과 GPS 모듈을 연결한 뒤 `ls /dev | grep 'ttyUSB'`를 실행하면 모듈이 `USB0`로 인식됩니다.

![장치 인식](../../en/06-jetson-nano-position-parse/images/2.jpg)

**3. 프로그램**

이번 장의 프로그램은 `GPS.py`입니다.

USB를 초기화합니다:

![코드](../../en/06-jetson-nano-position-parse/images/3.jpg)

위치 획득 및 파싱 함수는 수신 데이터에서 `GNGGA`로 시작하는 문장을 걸러 내어 전역 변수로 파싱합니다.

![코드](../../en/06-jetson-nano-position-parse/images/4.jpg)

![코드](../../en/06-jetson-nano-position-parse/images/5.jpg)

같은 방식으로 `GNVTG`에서 방향(heading) 정보를 읽어 파싱합니다.

![코드](../../en/06-jetson-nano-position-parse/images/6.jpg)

파싱한 데이터는 반복 출력됩니다.

![코드](../../en/06-jetson-nano-position-parse/images/7.jpg)

**4. 프로그램 실행**

터미널에서 `sudo python3 GPS.py`를 실행합니다.

**5. 결과**

전원을 켜면 모듈이 시작되는 데 약 32초가 걸립니다. 그 이후에는 시리얼 상태 LED가 계속 깜빡이며 데이터를 정상적으로 수신할 수 있습니다.

프로그램이 시작되면 USB를 초기화하고, 성공하면 `GPS Serial Opened! Baudrate=9600`을, 실패하면 `GPS Serial Open Failed!`를 출력합니다. 실패한 경우에는 배선이나 USB 포트를 확인하십시오. 그런 다음 위치와 방향 정보를 반복 출력합니다.

![출력](../../en/06-jetson-nano-position-parse/images/8.jpg)

Ctrl+C를 눌러 읽기를 중지합니다.

![종료](../../en/06-jetson-nano-position-parse/images/9.jpg)

모듈의 안테나는 반드시 실외에 두어야 하며, 그렇지 않으면 GPS 신호를 포착하지 못할 수 있습니다. 신호를 찾지 못하면 `GPS no found`를 출력합니다.
