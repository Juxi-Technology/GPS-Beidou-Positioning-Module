[English](../../en/05-stm32f103/gps-parse-output.md) | [Deutsch](../../de/05-stm32f103/gps-parse-output.md) | [Español](../../es/05-stm32f103/gps-parse-output.md) | [Français](../../fr/05-stm32f103/gps-parse-output.md) | [Italiano](../../it/05-stm32f103/gps-parse-output.md) | [日本語](../../ja/05-stm32f103/gps-parse-output.md) | 한국어 | [Português (BR)](../../pt-br/05-stm32f103/gps-parse-output.md) | [Português (PT)](../../pt-pt/05-stm32f103/gps-parse-output.md) | [简体中文](../../zh-hans/05-stm32f103/gps-parse-output.md) | [繁體中文](../../zh-hant/05-stm32f103/gps-parse-output.md)

**GPS 데이터 파싱 및 출력 (STM32)**

**1. 목표**

이번 장에서는 STM32F103C8T6과 GPS 모듈을 사용하여 위치 정보를 파싱하고 출력합니다.

**2. 준비**

GPS 모듈은 UART와 USB를 통해 통신합니다. 여기에서는 STM32의 UART를 사용합니다. 모듈의 TXD를 STM32F103C8T6 보드의 PA10 핀에, VCC와 GND를 보드의 5 V와 GND에 연결합니다. TTL 어댑터의 GND와 RXD를 STM32의 GND와 PA9에 연결합니다.

![배선](../../en/05-stm32f103/images/1.png)

**3. 프로그램**

모듈의 보드레이트는 9600입니다.

![코드](../../en/05-stm32f103/images/2.jpg)

수신한 데이터를 읽고 파싱합니다.

![코드](../../en/05-stm32f103/images/3.jpg)

위도 / 경도 단위를 도(degree)로 변환합니다.

![코드](../../en/05-stm32f103/images/4.jpg)

수신한 데이터를 시리얼 포트로 출력합니다.

![코드](../../en/05-stm32f103/images/5.jpg)

참고: GPS / BeiDou에서 얻은 위도와 경도는 단순히 ×100 관계가 아니며, 도-분 변환이 필요합니다. 예를 들어 위도 `2429.53531` N, 경도 `11810.78036` E인 경우:

```
24 + (29.53531 / 60) ≈ 24.49225517
118 + (10.78036 / 60) ≈ 118.17967267
```

마이크로컨트롤러에 따라 데이터 변환 정밀도 때문에 작은 오차가 발생할 수도 있습니다.

**4. 결과**

전원을 켜면 모듈이 시작되는 데 약 32초가 걸립니다. 그 이후에는 시리얼 상태 LED가 계속 깜빡이며 데이터를 정상적으로 수신할 수 있습니다.

프로그램을 다운로드하여 실행하고 9600 보드레이트로 시리얼 터미널을 열면 현재 위치 정보가 반복 출력됩니다.

![시리얼 출력](../../en/05-stm32f103/images/6.jpg)

모듈의 안테나는 반드시 실외에 두어야 하며, 그렇지 않으면 GPS 신호를 포착하지 못할 수 있습니다.
