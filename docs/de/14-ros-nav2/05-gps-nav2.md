[English](../../en/14-ros-nav2/05-gps-nav2.md) | Deutsch | [Español](../../es/14-ros-nav2/05-gps-nav2.md) | [Français](../../fr/14-ros-nav2/05-gps-nav2.md) | [Italiano](../../it/14-ros-nav2/05-gps-nav2.md) | [日本語](../../ja/14-ros-nav2/05-gps-nav2.md) | [한국어](../../ko/14-ros-nav2/05-gps-nav2.md) | [Português (BR)](../../pt-br/14-ros-nav2/05-gps-nav2.md) | [Português (PT)](../../pt-pt/14-ros-nav2/05-gps-nav2.md) | [简体中文](../../zh-hans/14-ros-nav2/05-gps-nav2.md) | [繁體中文](../../zh-hant/14-ros-nav2/05-gps-nav2.md)

### GPS- und Nav2-Navigation

**Um mit Nav2 zu einem gegebenen Breiten-/Längengrad zu navigieren, können Sie das Ziel nicht direkt senden — die Koordinaten müssen zuerst in Nav2-Ziel-xy-Werte umgerechnet werden. Dieser Abschnitt erläutert diese Umrechnung.**

#### 1. Ausführen

Nav2 muss bereits laufen. Es kann eine leere Karte geladen werden, aber die Ursprungs- und Zielkoordinaten müssen innerhalb dieser Karte liegen — andernfalls warnt das Programm `The goal sent to the planner is off the global costmap. Planning will always fail to this goal`, was bedeutet, dass der Planer sie nie erreichen wird. Das Starten von Nav2 wird hier nicht behandelt; wir gehen davon aus, dass es bereits läuft.

Mit laufendem Nav2 in einem Terminal:

```
ros2 launch gps_goal gps_goal.launch.py
```

- Geben Sie den Ursprungs-Breiten-/Längengrad an (wo bin ich?)

```
ros2 topic pub /local_xy_origin geometry_msgs/msg/PoseStamped "{header: {frame_id: 'map'}, pose: {position: {x: 43.658, y: -79.379}}}" -1
```

Dies veröffentlicht auf dem Topic `/local_xy_origin`. Die x- und y-Werte sind Beispiele und sollten an Ihre Situation angepasst werden.

Nach dem Ausführen gibt das Terminal `Received origin: lat -79.379, long 43.658` aus.

![Ursprung](../../en/14-ros-nav2/images/1.png)

- Geben Sie den Ziel-Breiten-/Längengrad an (wohin gehe ich?)

```
ros2 topic pub /gps_goal_fix sensor_msgs/msg/NavSatFix "{latitude: 2.548, longitude: 11.06455}" -1
```

Dies veröffentlicht auf `/gps_goal_fix`. Auch diese Koordinaten sind Beispiele.

Nach dem Ausführen gibt das Terminal aus:

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

![Zielausgabe](../../en/14-ros-nav2/images/2.png)

Aus der Ausgabe: Der Abstand zwischen den beiden Punkten beträgt **9284767.487 m** (weil die angegebenen Koordinaten extrem stark voneinander abweichen) und der Azimut ist **-32.818°**. Der umgerechnete Ziel-xy-Wert ist (7802896.906, -5032067.881) — eindeutig weit außerhalb der Karte, sodass die Planung ihn nie erreichen kann. Deshalb ist der frühere Hinweis wichtig: **Die Ursprungs- und Zielkoordinaten müssen innerhalb der Karte liegen.** Sobald die xy-Werte berechnet sind, werden sie zusammengepackt und zur Planung an Nav2 gesendet.

#### 2. Zum Quellcode

Quellpfad: `src/gps_goal/gps_goal/gps_goal.py` im Workspace.

Der Code ist einfach — sehen Sie sich die Hauptfunktion an:

```python
gps_goal_node = GpsGoalNode()  # create the object
lat, long = DMS_to_decimal_format(lat, long)  # parse the coordinates: from the command line and from the topic
gps_goal_node.do_gps_goal(lat, long, roll=roll, pitch=pitch, yaw=yaw)
```

Die Funktion `do_gps_goal`:

```python
def do_gps_goal(self, goal_lat, goal_long, z=0, yaw=0, roll=0, pitch=0):
    # Calculate goal x and y in the frame_id given the frame's origin GPS and a goal GPS location
    # convert lat/long into xy in the Nav2 map
    x, y = calc_goal(self.origin_lat, self.origin_long, goal_lat, goal_long)
    print("Goal x: ", x)
    print("Goal y: ", y)
    self.publish_goal(x=x, y=y, z=z, yaw=yaw, roll=roll, pitch=pitch)
```

`calc_goal` berechnet die xy-Werte aus den Ursprungs- und Zielkoordinaten. `publish_goal` packt die xy-Werte als `NavigateToPose.Goal()`-Nachricht zusammen und sendet sie über eine Action.

## Test mit einem gefälschten Nav2-Server

Öffnen Sie ein Terminal:

```
cd ~/GPS_ROS2
```

```
ros2 launch gps_goal gps_goal_demo.launch.py
```

Öffnen Sie ein neues Terminal:

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
