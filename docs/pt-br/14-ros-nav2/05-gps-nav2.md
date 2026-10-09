[English](../../en/14-ros-nav2/05-gps-nav2.md) | [Deutsch](../../de/14-ros-nav2/05-gps-nav2.md) | [Español](../../es/14-ros-nav2/05-gps-nav2.md) | [Français](../../fr/14-ros-nav2/05-gps-nav2.md) | [Italiano](../../it/14-ros-nav2/05-gps-nav2.md) | [日本語](../../ja/14-ros-nav2/05-gps-nav2.md) | [한국어](../../ko/14-ros-nav2/05-gps-nav2.md) | Português (BR) | [Português (PT)](../../pt-pt/14-ros-nav2/05-gps-nav2.md) | [简体中文](../../zh-hans/14-ros-nav2/05-gps-nav2.md) | [繁體中文](../../zh-hant/14-ros-nav2/05-gps-nav2.md)

### Navegação com GPS e Nav2

**Para navegar até uma latitude/longitude com o Nav2 você não pode enviar o objetivo diretamente — as coordenadas primeiro precisam ser convertidas em valores xy de objetivo do Nav2. Esta seção explica essa conversão.**

#### 1. Executando

O Nav2 já deve estar em execução. Um mapa em branco pode ser carregado, mas as coordenadas de origem e de destino devem estar dentro desse mapa — caso contrário, o programa avisa `The goal sent to the planner is off the global costmap. Planning will always fail to this goal`, o que significa que o planejador nunca chegará até ele. Iniciar o Nav2 não é abordado aqui; presumimos que ele já esteja no ar.

Com o Nav2 em execução, em um terminal:

```
ros2 launch gps_goal gps_goal.launch.py
```

- Informe a latitude/longitude de origem (onde estou?)

```
ros2 topic pub /local_xy_origin geometry_msgs/msg/PoseStamped "{header: {frame_id: 'map'}, pose: {position: {x: 43.658, y: -79.379}}}" -1
```

Isto publica no tópico `/local_xy_origin`. Os valores de x e y são exemplos e devem ser definidos de acordo com a sua situação.

Depois de executá-lo, o terminal imprime `Received origin: lat -79.379, long 43.658`.

![origem](../../en/14-ros-nav2/images/1.png)

- Informe a latitude/longitude do destino (para onde estou indo?)

```
ros2 topic pub /gps_goal_fix sensor_msgs/msg/NavSatFix "{latitude: 2.548, longitude: 11.06455}" -1
```

Isto publica em `/gps_goal_fix`. Estas coordenadas também são exemplos.

Depois de executá-lo, o terminal imprime:

```
[INFO] [gps_goal_node]: The distance from the origin to the goal is 9284767.487 m.
[INFO] [gps_goal_node]: The azimuth from the origin to the goal is -32.818 degrees.
[INFO] [gps_goal_node]: The translation from the origin to the goal is (x,y) 7802896.906, -5032067.881 m.
Goal x:  7802896.905971293
Goal y:  -5032067.881259187
[INFO] [gps_goal_node]: Executing Nav2 goal to position (x,y) 7802896.906, -5032067.881, with 0 degrees yaw.
[INFO] [gps_goal_node]: To cancel the goal: 'ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose --cancel'
[INFO] [gps_goal_node]: Initial goal status: ACCEPTED
[INFO] [gps_goal_node]: This goal has been accepted by the action server
[INFO] [gps_goal_node]: Final goal status: ABORTED
[INFO] [gps_goal_node]: Failed to find a valid plan. Even after executing recovery behaviors.
```

![saída do objetivo](../../en/14-ros-nav2/images/2.png)

Pela saída: a distância entre os dois pontos é **9284767.487 m** (porque as coordenadas informadas diferem enormemente) e o azimute é **-32.818°**. O valor xy de destino convertido é (7802896.906, -5032067.881) — claramente muito fora do mapa, então o planejamento nunca consegue chegar até ele. É por isso que a observação anterior importa: **as coordenadas de origem e de destino devem estar dentro do mapa.** Depois que os valores xy são calculados, eles são empacotados e enviados ao Nav2 para planejamento.

#### 2. Sobre o código-fonte

Caminho do código-fonte: `src/gps_goal/gps_goal/gps_goal.py` no workspace.

O código é simples — veja a função principal:

```python
gps_goal_node = GpsGoalNode()  # create the object
lat, long = DMS_to_decimal_format(lat, long)  # parse the coordinates: from the command line and from the topic
gps_goal_node.do_gps_goal(lat, long, roll=roll, pitch=pitch, yaw=yaw)
```

A função `do_gps_goal`:

```python
def do_gps_goal(self, goal_lat, goal_long, z=0, yaw=0, roll=0, pitch=0):
    # Calculate goal x and y in the frame_id given the frame's origin GPS and a goal GPS location
    # convert lat/long into xy in the Nav2 map
    x, y = calc_goal(self.origin_lat, self.origin_long, goal_lat, goal_long)
    print("Goal x: ", x)
    print("Goal y: ", y)
    self.publish_goal(x=x, y=y, z=z, yaw=yaw, roll=roll, pitch=pitch)
```

`calc_goal` calcula os valores xy a partir das coordenadas de origem e de destino. `publish_goal` empacota os valores xy como uma mensagem `NavigateToPose.Goal()` e a envia por uma action.

## Testando com um servidor Nav2 falso

Abra um terminal:

```
cd ~/GPS_ROS2
```

```
ros2 launch gps_goal gps_goal_demo.launch.py
```

Abra um novo terminal:

```
# set the origin
ros2 topic pub --once /local_xy_origin geometry_msgs/msg/PoseStamped "{
  header: {frame_id: 'map'},
  pose: {position: {x: 0.0, y: 0.0}}
}"
```

```
# set the goal (5 metres north)
ros2 topic pub --once /gps_goal_fix sensor_msgs/msg/NavSatFix "{
  latitude: 0.000045, longitude: 0.0
}"
```
