[English](../../en/07-jetson-nano-agnss/agnss.md) | [Deutsch](../../de/07-jetson-nano-agnss/agnss.md) | [Español](../../es/07-jetson-nano-agnss/agnss.md) | [Français](../../fr/07-jetson-nano-agnss/agnss.md) | [Italiano](../../it/07-jetson-nano-agnss/agnss.md) | [日本語](../../ja/07-jetson-nano-agnss/agnss.md) | 한국어 | [Português (BR)](../../pt-br/07-jetson-nano-agnss/agnss.md) | [Português (PT)](../../pt-pt/07-jetson-nano-agnss/agnss.md) | [简体中文](../../zh-hans/07-jetson-nano-agnss/agnss.md) | [繁體中文](../../zh-hant/07-jetson-nano-agnss/agnss.md)

**AGNSS 보조 측위**

**1. 목표**

이번 장에서는 Jetson Orin, GPS 모듈, AGNSS 서버를 사용하여 약신호 환경에서 위치 정보를 읽고 파싱합니다.

**2. AGNSS 소개**

2.1 **AGNSS가 필요한 이유**

- 독립형 GNSS 수신기는 위치를 확정하기 전에 위성 신호를 포착·추적하고 항법 메시지를 복호화해야 합니다.
- 강신호 환경에서는 약 30초 만에 콜드 스타트할 수 있습니다. 약신호 환경에서는 포착이 느리고 항법 메시지 복호화가 어려워, 위치 확정에 매우 오랜 시간이 걸리거나 아예 이루어지지 않을 수 있습니다.
- AGNSS는 수신기에 필요한 보조 정보, 즉 항법 데이터와 대략적인 위치 및 시각을 제공합니다. 강신호와 약신호 조건 모두에서 최초 위치 획득 시간(TTFF)을 크게 단축합니다.

2.2 **동작 원리**

- AGNSS 서버는 여러 GNSS 소스로부터 보조 데이터를 수집·관리하며, 클라이언트 요청(사용자 이름과 비밀번호 필요)에 응답합니다.
- 클라이언트는 TCP/IP를 통해 보조 데이터를 가져와 GNSS 수신기로 전달합니다.
- 자체 프록시 서버를 운영할 수도 있습니다.

![아키텍처](../../en/07-jetson-nano-agnss/images/1.png)

2.3 **절차**

- AGNSS 서버에 연결
  - 주소: `121.41.40.95` (도메인 `www.gnss-aide.com`)
  - 포트: `2621`
- AGNSS 요청 전송
  - 요청 문자열(사용자 이름과 비밀번호 필요):
  - `user=<your-username>;pwd=<your-password>;cmd=full;gnss=gps+bd;lat=60.0;lon=55.0;alt=0;`
- 보조 데이터 수신
- 수신기로 전달

2.4 **요청 파라미터**

요청은 `key=value;` 쌍의 나열이며, 예를 들어 `key=value;key=value;`와 같습니다.

예: `user=<your-username>;pwd=<your-password>;cmd=full;gnss=gps+bd;lat=60.0;lon=55.0;alt=0;`

| 키 | 값 | 필수 | 비고 |
| --- | --- | --- | --- |
| **user** | string | yes | 사용자 이름. 유효한 이메일 주소 사용을 강력히 권장합니다. 중요한 AGNSS 서버 유지보수 공지가 이 주소로 발송됩니다. |
| **pwd** | string | yes | 사용자 비밀번호 |
| **gnss** | string | no | 쉼표로 구분된 GNSS 목록이며, 현재 GPS를 지원합니다. 유효한 값은 `gps`, `bds`, `glo`입니다. `gnss=gps;`는 GPS 보조를 요청하고, `gnss=gps,bds;`는 GPS와 BDS 보조를 요청합니다. |
| **cmd** | string | no | `full`: ephemeris, 추정 시각 및 위치를 포함한 모든 정보. `eph`: ephemeris만. `aid`: 보조 시각 및 위치. 기본값은 `full`입니다. |
| **lat** | number | no | 사용자의 추정 위도(도 단위, -90 ~ 90). 위치 보조는 lat/lon/alt 또는 ECEF 두 형식이 있으며 하나를 선택합니다. lat/lon/alt 형식은 세 필드가 모두 필요합니다: `lat=30;lon=120.3;alt=100;` |
| **lon** | number | no | 사용자의 추정 경도(도 단위, -180 ~ 180). |
| **alt** | number | no | 사용자의 추정 고도(미터 단위). |
| **x** | number | no | 사용자의 추정 ECEF X(미터 단위). ECEF 형식은 세 필드가 모두 필요합니다: `x=30000;y=1111120.3;z=3345100;` |
| **y** | number | no | 사용자의 추정 ECEF Y(미터 단위). |
| **z** | number | no | 사용자의 추정 ECEF Z(미터 단위). |
| **pacc** | number | no | 사용자 위치의 정확도(미터 단위). |

2.5 **서버 응답**

![응답](../../en/07-jetson-nano-agnss/images/2.png)

- 서버는 데이터 헤더에 이어 보조 데이터를 반환합니다.
- 바이너리 페이로드는 수신기에 필요한 보조 데이터이며 자체 체크섬을 포함합니다. 바이너리 형식은 CASIC 수신기 프로토콜 명세서를 참조하십시오.
- 헤더도 함께 수신기로 전달해도 무방합니다.

2.6 **성능**

독립형 GNSS 수신기와 비교할 때 AGNSS 수신기는 특히 약신호 조건에서 TTFF를 크게 개선합니다.

![TTFF 비교](../../en/07-jetson-nano-agnss/images/3.jpg)

2.7 **참고 사항**

- 대략적인 위치는 다른 방법으로 얻어야 하며, 예를 들면 다음과 같습니다:
  - GSM/GPRS/3G 모듈: 셀 ID로부터 대략적인 위치를 도출할 수 있습니다
  - Wi-Fi 또는 기타 무선 모듈: 마찬가지로 대략적인 측위가 가능합니다
- 대략적인 위치는 15 km 이내의 정확도를 가져야 하며, 잘못된 위치 힌트는 수신기 성능을 저하시킵니다.
- 대략적인 위치를 알 수 없다면 요청에서 위치 필드(lat, lon, alt, x, y, z)를 생략하십시오. 그러면 수신기는 마지막으로 유효했던 측위 결과로 폴백합니다.
- 수신기 자체의 출력을 대략적인 위치로 사용할 필요는 없습니다.

2.8 **AGNSS가 필요한 시점**

부팅할 때마다 서버에서 다운로드할 필요는 없으며, 이는 대역폭을 절약합니다:

- CASIC 칩에는 수신한 ephemeris 데이터를 보존하는 배터리 백업 SRAM과 영구 백업 flash가 있습니다.
- 정상 동작 중에는 칩이 위성으로부터 최신 ephemeris를 계속 다운로드합니다.
- 수신기 상태를 조회하여 다운로드가 필요한지 판단할 수 있습니다. 수신기는 항법 메시지 상태 문장을 출력할 수 있습니다(기본값은 꺼짐이며, 설정이 필요합니다).

2.9 **항법 메시지 상태 문장**

![문장 1](../../en/07-jetson-nano-agnss/images/4.png)

![문장 2](../../en/07-jetson-nano-agnss/images/5.png)

- 이 문장은 수신기의 내부 시각과 항법 메시지 상태를 보고합니다.
- `$PCAS03,,,,,,,,,,,1*1F`를 보내면 1초에 한 번 출력합니다.
- `$PCAS03,,,,,,,,,,,0*1E`를 보내면 출력을 중지합니다.
- 참고: 모든 문장은 `\r\n`(0x0D, 0x0A)으로 끝나야 하며, 쉼표를 11개 포함합니다.
- 시간 플래그가 유효하고(0이 아니고) 유효한 ephemeris 개수가 많으면(8개 초과) AGNSS ephemeris를 다운로드할 필요가 없습니다.

**3. 준비**

**3.1 배선**

GPS 모듈은 UART 또는 USB 통신을 지원하며, 여기에서는 USB를 사용합니다.

![배선](../../en/07-jetson-nano-agnss/images/6.png)

Type-C 케이블로 Jetson Orin과 GPS 모듈을 연결한 뒤 `ls /dev | grep 'ttyUSB'`를 실행하면 모듈이 `USB0`로 인식됩니다.

![장치 인식](../../en/07-jetson-nano-agnss/images/7.jpg)

**3.2 Baidu Map AK 발급**

[Baidu Map API 키 신청](baidu-map-api-key.md)을 참조하십시오.

**4. 프로그램**

이번 장의 프로그램은 `GPS-agnss.py`입니다.

USB를 초기화합니다:

![코드](../../en/07-jetson-nano-agnss/images/8.jpg)

신청한 AK를 입력하면 Baidu Maps에서 현재의 대략적인 위도와 경도를 읽을 수 있습니다.

![코드](../../en/07-jetson-nano-agnss/images/9.jpg)

Baidu Maps에서 얻은 대략적인 좌표를 서버로 전송하며(자신의 AGNSS 계정 사용), 완료되면 전체 패킷을 모듈로 전송합니다.

![코드](../../en/07-jetson-nano-agnss/images/10.jpg)

![코드](../../en/07-jetson-nano-agnss/images/11.jpg)

위치 획득 및 파싱 함수는 수신 데이터에서 `GNGGA`로 시작하는 문장을 걸러 내어 전역 변수로 파싱합니다.

![코드](../../en/07-jetson-nano-agnss/images/12.jpg)

![코드](../../en/07-jetson-nano-agnss/images/13.jpg)

같은 방식으로 `GNVTG`에서 방향(heading) 정보를 읽어 파싱합니다.

![코드](../../en/07-jetson-nano-agnss/images/14.jpg)

파싱한 데이터는 반복 출력됩니다.

![코드](../../en/07-jetson-nano-agnss/images/15.jpg)

**5. 프로그램 실행**

터미널에서 `sudo python2 GPS-agnss.py`를 실행합니다.

**6. 결과**

**참고: 보조 측위를 사용할 때 Jetson Orin은 네트워크에 연결되어 있어야 합니다.**

약신호 환경에서 전원을 켜면 프로그램이 USB를 초기화하고, 성공하면 `GPS Serial Opened! Baudrate=9600`을, 실패하면 `GPS Serial Open Failed!`를 출력합니다. 실패한 경우에는 배선이나 USB 포트를 확인하십시오.

그런 다음 서버로 보조 데이터를 전송하면서 `GPS Agnss start`를, 완료되면 `GPS Agnss success`를 출력합니다.

GPS 신호를 획득할 때까지는 Baidu Maps에서 읽은 대략적인 좌표와 함께 `GPS no found`를 출력합니다.

![출력](../../en/07-jetson-nano-agnss/images/16.jpg)

신호를 획득하면 위치와 방향 정보를 반복 출력합니다.

![출력](../../en/07-jetson-nano-agnss/images/17.jpg)

Ctrl+C를 눌러 읽기를 중지합니다.
