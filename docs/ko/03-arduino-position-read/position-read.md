[English](../../en/03-arduino-position-read/position-read.md) | [Deutsch](../../de/03-arduino-position-read/position-read.md) | [Español](../../es/03-arduino-position-read/position-read.md) | [Français](../../fr/03-arduino-position-read/position-read.md) | [Italiano](../../it/03-arduino-position-read/position-read.md) | [日本語](../../ja/03-arduino-position-read/position-read.md) | 한국어 | [Português (BR)](../../pt-br/03-arduino-position-read/position-read.md) | [Português (PT)](../../pt-pt/03-arduino-position-read/position-read.md) | [简体中文](../../zh-hans/03-arduino-position-read/position-read.md) | [繁體中文](../../zh-hant/03-arduino-position-read/position-read.md)

**GPS 위치 데이터 읽기**

**1. 목표**

이번 장에서는 Arduino와 GPS 모듈을 사용하여 위치 정보를 읽습니다.

**2. 준비**

GPS 모듈은 UART와 USB를 통해 통신합니다. 여기에서는 Arduino UNO의 UART를 사용합니다. 모듈의 TX를 UNO의 D0 핀에, VCC와 GND를 5 V와 GND에 연결합니다.

![배선](../../en/03-arduino-position-read/images/1.png)

**3. 프로그램**

시리얼 포트를 초기화합니다.

![코드](../../en/03-arduino-position-read/images/2.jpg)

수신한 데이터를 출력합니다.

**4. 컴파일 및 업로드**

4.1 Arduino IDE에서 파일을 열고 툴바의 "✓" 버튼을 클릭하여 컴파일한 뒤, 상태 표시줄에 "Done compiling"이 나타날 때까지 기다립니다.

![컴파일](../../en/03-arduino-position-read/images/3.jpg)

4.2 Arduino IDE 메뉴에서 Tools → Port → 장치 관리자에 표시된 포트를 선택합니다.

![포트 선택](../../en/03-arduino-position-read/images/4.jpg)

4.3 그런 다음 "→" 버튼을 클릭하여 코드를 UNO 보드에 업로드합니다. "Done uploading"이 나타나면 업로드에 성공한 것입니다.

![업로드](../../en/03-arduino-position-read/images/5.jpg)

**5. 결과**

전원을 켜면 모듈이 시작되는 데 약 32초가 걸립니다. 그 이후에는 시리얼 상태 LED가 계속 깜빡이며 데이터를 정상적으로 수신할 수 있습니다.

프로그램을 실행하고 시리얼 모니터를 열어 보드레이트를 9600으로 설정합니다. 현재 위치 정보가 반복 출력됩니다. 이는 가공되지 않은 원시 데이터이며, 각 문장(sentence)의 의미는 [CASIC GNSS 프로토콜 명세서](../../../docs/datasheets/CASIC-GNSS-protocol-spec-CN.pdf)를 참조하십시오.

![시리얼 출력](../../en/03-arduino-position-read/images/6.jpg)

모듈의 안테나는 반드시 실외에 두어야 하며, 그렇지 않으면 GPS 신호를 포착하지 못할 수 있습니다.
