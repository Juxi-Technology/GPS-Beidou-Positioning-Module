[English](../../en/04-arduino-position-parse/position-parse.md) | [Deutsch](../../de/04-arduino-position-parse/position-parse.md) | [Español](../../es/04-arduino-position-parse/position-parse.md) | [Français](../../fr/04-arduino-position-parse/position-parse.md) | [Italiano](../../it/04-arduino-position-parse/position-parse.md) | [日本語](../../ja/04-arduino-position-parse/position-parse.md) | 한국어 | [Português (BR)](../../pt-br/04-arduino-position-parse/position-parse.md) | [Português (PT)](../../pt-pt/04-arduino-position-parse/position-parse.md) | [简体中文](../../zh-hans/04-arduino-position-parse/position-parse.md) | [繁體中文](../../zh-hant/04-arduino-position-parse/position-parse.md)

**GPS 위치 데이터 파싱**

**1. 목표**

이번 장에서는 Arduino와 GPS 모듈을 사용하여 위치 정보를 파싱하고 출력합니다.

**2. 준비**

GPS 모듈은 UART와 USB를 통해 통신합니다. 여기에서는 Arduino UNO의 UART를 사용합니다. 모듈의 TX를 UNO의 D0 핀에, VCC와 GND를 5 V와 GND에 연결합니다.

![배선](../../en/04-arduino-position-parse/images/1.png)

**3. 프로그램**

시리얼 포트를 초기화합니다.

![코드](../../en/04-arduino-position-parse/images/2.jpg)

시리얼 데이터를 읽습니다.

![코드](../../en/04-arduino-position-parse/images/3.jpg)

시리얼 데이터를 파싱합니다.

![코드](../../en/04-arduino-position-parse/images/4.jpg)

파싱한 위치 정보를 출력합니다.

![코드](../../en/04-arduino-position-parse/images/5.jpg)

**4. 컴파일 및 업로드**

4.1 Arduino IDE에서 파일을 열고 "✓" 버튼을 클릭하여 컴파일한 뒤 "Done compiling"이 나타날 때까지 기다립니다.

![컴파일](../../en/04-arduino-position-parse/images/6.jpg)

4.2 메뉴에서 Tools → Port → 장치 관리자에 표시된 포트를 선택합니다.

![포트 선택](../../en/04-arduino-position-parse/images/7.jpg)

4.3 "→" 버튼을 클릭하여 업로드합니다. "Done uploading"이 나타나면 업로드에 성공한 것입니다.

![업로드](../../en/04-arduino-position-parse/images/8.jpg)

**5. 결과**

전원을 켜면 모듈이 시작되는 데 약 32초가 걸립니다. 그 이후에는 시리얼 상태 LED가 계속 깜빡이며 데이터를 정상적으로 수신할 수 있습니다.

프로그램을 실행하고 9600 보드레이트로 시리얼 모니터를 열면 파싱된 실시간 위치 정보가 반복 출력됩니다.

![시리얼 출력](../../en/04-arduino-position-parse/images/9.jpg)

모듈의 안테나는 반드시 실외에 두어야 하며, 그렇지 않으면 GPS 신호를 포착하지 못할 수 있습니다.
