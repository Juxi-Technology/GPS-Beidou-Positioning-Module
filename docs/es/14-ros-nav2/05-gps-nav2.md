[English](../../en/14-ros-nav2/05-gps-nav2.md) | [Deutsch](../../de/14-ros-nav2/05-gps-nav2.md) | Español | [Français](../../fr/14-ros-nav2/05-gps-nav2.md) | [Italiano](../../it/14-ros-nav2/05-gps-nav2.md) | [日本語](../../ja/14-ros-nav2/05-gps-nav2.md) | [한국어](../../ko/14-ros-nav2/05-gps-nav2.md) | [Português (BR)](../../pt-br/14-ros-nav2/05-gps-nav2.md) | [Português (PT)](../../pt-pt/14-ros-nav2/05-gps-nav2.md) | [简体中文](../../zh-hans/14-ros-nav2/05-gps-nav2.md) | [繁體中文](../../zh-hant/14-ros-nav2/05-gps-nav2.md)

### Navegación con GPS y Nav2

**Para navegar a una latitud/longitud determinada con Nav2 no puedes enviar el objetivo directamente: primero hay que convertir las coordenadas en valores xy de objetivo de Nav2. Esta sección explica esa conversión.**

#### 1. Ejecución

Nav2 debe estar ya en ejecución. Se puede cargar un mapa en blanco, pero las coordenadas de origen y de objetivo deben estar dentro de ese mapa; de lo contrario, el programa advierte `The goal sent to the planner is off the global costmap. Planning will always fail to this goal`, lo que significa que el planificador nunca lo alcanzará. Aquí no se explica cómo iniciar Nav2; damos por hecho que ya está en marcha.

Con Nav2 en ejecución, en un terminal:

```
ros2 launch gps_goal gps_goal.launch.py
```

- Indica la latitud/longitud de origen (¿dónde estoy?)

```
ros2 topic pub /local_xy_origin geometry_msgs/msg/PoseStamped "{header: {frame_id: 'map'}, pose: {position: {x: 43.658, y: -79.379}}}" -1
```

Esto publica en el topic `/local_xy_origin`. Los valores de x e y son ejemplos y deben ajustarse a tu situación.

Después de ejecutarlo, el terminal imprime `Received origin: lat -79.379, long 43.658`.

![origen](../../en/14-ros-nav2/images/1.png)

- Indica la latitud/longitud del objetivo (¿adónde voy?)

```
ros2 topic pub /gps_goal_fix sensor_msgs/msg/NavSatFix "{latitude: 2.548, longitude: 11.06455}" -1
```

Esto publica en `/gps_goal_fix`. Estas coordenadas también son ejemplos.

Después de ejecutarlo, el terminal imprime:

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

![salida del objetivo](../../en/14-ros-nav2/images/2.png)

Según la salida: la distancia entre los dos puntos es **9284767.487 m** (porque las coordenadas indicadas difieren enormemente) y el azimut es **-32.818°**. El valor xy del objetivo convertido es (7802896.906, -5032067.881), claramente muy fuera del mapa, por lo que el planificador nunca podrá alcanzarlo. Por eso es importante la nota anterior: **las coordenadas de origen y de objetivo deben estar dentro del mapa.** Una vez calculados los valores xy, se empaquetan y se envían a Nav2 para su planificación.

#### 2. Acerca del código fuente

Ruta del código fuente: `src/gps_goal/gps_goal/gps_goal.py` en el espacio de trabajo.

El código es sencillo; fíjate en la función main:

```python
gps_goal_node = GpsGoalNode()  # create the object
lat, long = DMS_to_decimal_format(lat, long)  # parse the coordinates: from the command line and from the topic
gps_goal_node.do_gps_goal(lat, long, roll=roll, pitch=pitch, yaw=yaw)
```

La función `do_gps_goal`:

```python
def do_gps_goal(self, goal_lat, goal_long, z=0, yaw=0, roll=0, pitch=0):
    # Calculate goal x and y in the frame_id given the frame's origin GPS and a goal GPS location
    # convert lat/long into xy in the Nav2 map
    x, y = calc_goal(self.origin_lat, self.origin_long, goal_lat, goal_long)
    print("Goal x: ", x)
    print("Goal y: ", y)
    self.publish_goal(x=x, y=y, z=z, yaw=yaw, roll=roll, pitch=pitch)
```

`calc_goal` calcula los valores xy a partir de las coordenadas de origen y de objetivo. `publish_goal` empaqueta los valores xy como un mensaje `NavigateToPose.Goal()` y lo envía mediante una action.

## Prueba con un servidor Nav2 simulado

Abre un terminal:

```
cd ~/GPS_ROS2
```

```
ros2 launch gps_goal gps_goal_demo.launch.py
```

Abre un nuevo terminal:

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
