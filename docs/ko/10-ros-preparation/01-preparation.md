[English](../../en/10-ros-preparation/01-preparation.md) | [Deutsch](../../de/10-ros-preparation/01-preparation.md) | [Español](../../es/10-ros-preparation/01-preparation.md) | [Français](../../fr/10-ros-preparation/01-preparation.md) | [Italiano](../../it/10-ros-preparation/01-preparation.md) | [日本語](../../ja/10-ros-preparation/01-preparation.md) | 한국어 | [Português (BR)](../../pt-br/10-ros-preparation/01-preparation.md) | [Português (PT)](../../pt-pt/10-ros-preparation/01-preparation.md) | [简体中文](../../zh-hans/10-ros-preparation/01-preparation.md) | [繁體中文](../../zh-hant/10-ros-preparation/01-preparation.md)

### 시작하기 전에

#### 1. GPS 패키지 빌드

(1) 워크스페이스를 만들고 `gps_src` 폴더의 내용을 워크스페이스의 `src` 디렉터리에 복사한 다음, `colcon build`로 빌드합니다. 오류가 나타나지 않으면 빌드에 성공한 것입니다.

`~/gps_ros2`에서:

```
colcon build
```

그런 다음 `~/gps_ros2`에서:

```
source install/setup.bash
```

(2) 각 패키지의 내용:

- `nmea_navsat_driver` — GPS 모듈 구동, 데이터 읽기, GPS 궤적 그리기
- `nmea_msgs` — GPS 관련 메시지의 메시지 정의
- `imu_gps_localization` — IMU와 GPS 데이터 융합
- `gps_goal` — 위도/경도를 Nav2 goal로 변환

#### 2. GPS 모듈에 고정 포트 바인딩

GPS 모듈은 직렬 포트를 통해 PC 또는 호스트와 통신하므로, 고정 포트 이름을 바인딩합니다. 그렇지 않으면 포트 번호가 바뀌면서 호스트가 모듈을 찾지 못할 수 있습니다.

(1) 연결된 USB 장치를 나열하여 GPS 모듈을 찾습니다. **lsusb**를 실행하고 아래와 같이 장치 ID를 확인합니다.

![lsusb 출력](../../en/10-ros-preparation/images/1.png)

(2) 장치 ID를 확인했으면 udev 규칙 파일을 작성하여 포트를 바인딩합니다. 다음을 실행합니다:

```
sudo gedit /etc/udev/rules.d/my_serial.rules
```

그리고 다음을 붙여 넣습니다:

```
KERNEL=="ttyUSB*", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", MODE:="0777", SYMLINK+="myserial"
```

저장하고 종료한 뒤 실행 권한을 부여합니다:

```
sudo chmod 777 /etc/udev/rules.d/my_serial.rules
```

(3) GPS 모듈을 뽑았다가 다시 꽂은 뒤 `ll /dev/myserial`을 실행하여 바인딩이 되었는지 확인합니다. 아래 출력이 나오면 성공한 것입니다.

```
ll /dev/myserial
```

![udev 바인딩](../../en/10-ros-preparation/images/2.png)
