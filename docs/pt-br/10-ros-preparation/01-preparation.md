[English](../../en/10-ros-preparation/01-preparation.md) | [Deutsch](../../de/10-ros-preparation/01-preparation.md) | [Español](../../es/10-ros-preparation/01-preparation.md) | [Français](../../fr/10-ros-preparation/01-preparation.md) | [Italiano](../../it/10-ros-preparation/01-preparation.md) | [日本語](../../ja/10-ros-preparation/01-preparation.md) | [한국어](../../ko/10-ros-preparation/01-preparation.md) | Português (BR) | [Português (PT)](../../pt-pt/10-ros-preparation/01-preparation.md) | [简体中文](../../zh-hans/10-ros-preparation/01-preparation.md) | [繁體中文](../../zh-hant/10-ros-preparation/01-preparation.md)

### Antes de começar

#### 1. Compilando os pacotes do GPS

(1) Crie um workspace, copie o conteúdo da pasta `gps_src` para o diretório `src` do workspace e compile com `colcon build`. Se nenhum erro aparecer, a compilação foi bem-sucedida.

Em `~/gps_ros2`:

```
colcon build
```

Em seguida, em `~/gps_ros2`:

```
source install/setup.bash
```

(2) O que cada pacote contém:

- `nmea_navsat_driver` — iniciar o módulo GPS, ler seus dados e desenhar as trajetórias do GPS
- `nmea_msgs` — definições das mensagens relacionadas ao GPS
- `imu_gps_localization` — fusão dos dados de IMU e GPS
- `gps_goal` — conversão de latitude/longitude em um objetivo do Nav2

#### 2. Vinculando uma porta fixa ao módulo GPS

O módulo GPS se comunica com o PC ou host por uma porta serial, então vinculamos um nome de porta fixo a ele — caso contrário, um número de porta variável pode impedir o host de encontrar o módulo.

(1) Liste os dispositivos USB conectados e localize o módulo GPS. Execute **lsusb** e anote o ID do dispositivo, como mostrado abaixo.

![saída do lsusb](../../en/10-ros-preparation/images/1.png)

(2) Com o ID do dispositivo em mãos, escreva um arquivo de regras udev para vincular a porta. Execute:

```
sudo gedit /etc/udev/rules.d/my_serial.rules
```

e cole o seguinte:

```
KERNEL=="ttyUSB*", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", MODE:="0777", SYMLINK+="myserial"
```

Salve, saia e torne-o executável:

```
sudo chmod 777 /etc/udev/rules.d/my_serial.rules
```

(3) Desconecte e reconecte o módulo GPS e execute `ll /dev/myserial` para verificar se a vinculação funcionou. A saída abaixo significa que deu certo.

```
ll /dev/myserial
```

![vinculação udev](../../en/10-ros-preparation/images/2.png)
