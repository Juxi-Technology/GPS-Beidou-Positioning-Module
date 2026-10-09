[English](../../en/10-ros-preparation/01-preparation.md) | [Deutsch](../../de/10-ros-preparation/01-preparation.md) | [Español](../../es/10-ros-preparation/01-preparation.md) | [Français](../../fr/10-ros-preparation/01-preparation.md) | [Italiano](../../it/10-ros-preparation/01-preparation.md) | [日本語](../../ja/10-ros-preparation/01-preparation.md) | [한국어](../../ko/10-ros-preparation/01-preparation.md) | [Português (BR)](../../pt-br/10-ros-preparation/01-preparation.md) | Português (PT) | [简体中文](../../zh-hans/10-ros-preparation/01-preparation.md) | [繁體中文](../../zh-hant/10-ros-preparation/01-preparation.md)

### Antes de Começar

#### 1. Compilar os pacotes do GPS

(1) Crie um workspace, copie o conteúdo da pasta `gps_src` para o diretório `src` do workspace e, em seguida, compile com `colcon build`. Se não aparecerem erros, a compilação foi bem-sucedida.

Em `~/gps_ros2`:

```
colcon build
```

Em seguida, em `~/gps_ros2`:

```
source install/setup.bash
```

(2) O que contém cada pacote:

- `nmea_navsat_driver` — iniciar o módulo GPS, ler os seus dados e desenhar as trajetórias do GPS
- `nmea_msgs` — definições das mensagens relacionadas com o GPS
- `imu_gps_localization` — fusão de dados de IMU e GPS
- `gps_goal` — conversão de latitude/longitude num objetivo do Nav2

#### 2. Associar uma porta fixa ao módulo GPS

O módulo GPS comunica com o PC ou host através de uma porta série, por isso associamos-lhe um nome de porta fixo — caso contrário, um número de porta variável pode impedir o host de encontrar o módulo.

(1) Liste os dispositivos USB ligados e localize o módulo GPS. Execute **lsusb** e anote o ID do dispositivo, como mostrado abaixo.

![saída do lsusb](../../en/10-ros-preparation/images/1.png)

(2) Com o ID do dispositivo conhecido, escreva um ficheiro de regras udev para associar a porta. Execute:

```
sudo gedit /etc/udev/rules.d/my_serial.rules
```

e cole o seguinte:

```
KERNEL=="ttyUSB*", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", MODE:="0777", SYMLINK+="myserial"
```

Guarde, saia e torne-o executável:

```
sudo chmod 777 /etc/udev/rules.d/my_serial.rules
```

(3) Desligue e volte a ligar o módulo GPS e, em seguida, execute `ll /dev/myserial` para verificar se a associação funcionou. A saída abaixo significa que foi bem-sucedido.

```
ll /dev/myserial
```

![associação udev](../../en/10-ros-preparation/images/2.png)
