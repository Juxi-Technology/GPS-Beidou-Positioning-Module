[English](../../en/14-ros-nav2/05-gps-nav2.md) | [Deutsch](../../de/14-ros-nav2/05-gps-nav2.md) | [Español](../../es/14-ros-nav2/05-gps-nav2.md) | Français | [Italiano](../../it/14-ros-nav2/05-gps-nav2.md) | [日本語](../../ja/14-ros-nav2/05-gps-nav2.md) | [한국어](../../ko/14-ros-nav2/05-gps-nav2.md) | [Português (BR)](../../pt-br/14-ros-nav2/05-gps-nav2.md) | [Português (PT)](../../pt-pt/14-ros-nav2/05-gps-nav2.md) | [简体中文](../../zh-hans/14-ros-nav2/05-gps-nav2.md) | [繁體中文](../../zh-hant/14-ros-nav2/05-gps-nav2.md)

### Navigation GPS et Nav2

**Pour naviguer vers une latitude/longitude donnée avec Nav2, vous ne pouvez pas envoyer l'objectif directement — les coordonnées doivent d'abord être converties en valeurs xy d'objectif Nav2. Cette section explique cette conversion.**

#### 1. Exécution

Nav2 doit déjà être en cours d'exécution. Une carte vide peut être chargée, mais les coordonnées d'origine et d'objectif doivent se trouver à l'intérieur de cette carte — sinon le programme avertit `The goal sent to the planner is off the global costmap. Planning will always fail to this goal`, ce qui signifie que le planificateur ne l'atteindra jamais. Le démarrage de Nav2 n'est pas traité ici ; nous supposons qu'il est déjà lancé.

Une fois Nav2 lancé, dans un terminal :

```
ros2 launch gps_goal gps_goal.launch.py
```

- Indiquez la latitude/longitude d'origine (où suis-je ?)

```
ros2 topic pub /local_xy_origin geometry_msgs/msg/PoseStamped "{header: {frame_id: 'map'}, pose: {position: {x: 43.658, y: -79.379}}}" -1
```

Cela publie sur le topic `/local_xy_origin`. Les valeurs x et y sont des exemples et doivent être définies selon votre situation.

Après l'exécution, le terminal affiche `Received origin: lat -79.379, long 43.658`.

![origine](../../en/14-ros-nav2/images/1.png)

- Indiquez la latitude/longitude de l'objectif (où vais-je ?)

```
ros2 topic pub /gps_goal_fix sensor_msgs/msg/NavSatFix "{latitude: 2.548, longitude: 11.06455}" -1
```

Cela publie sur `/gps_goal_fix`. Ces coordonnées sont également des exemples.

Après l'exécution, le terminal affiche :

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

![sortie de l'objectif](../../en/14-ros-nav2/images/2.png)

D'après la sortie : la distance entre les deux points est de **9284767.487 m** (car les coordonnées indiquées diffèrent énormément) et l'azimut est de **-32.818°**. La valeur xy d'objectif convertie est (7802896.906, -5032067.881) — clairement bien au-delà de la carte, le planificateur ne peut donc jamais l'atteindre. C'est pourquoi la remarque précédente est importante : **les coordonnées d'origine et d'objectif doivent se trouver à l'intérieur de la carte.** Une fois les valeurs xy calculées, elles sont empaquetées et envoyées à Nav2 pour la planification.

#### 2. À propos du code source

Chemin du code source : `src/gps_goal/gps_goal/gps_goal.py` dans l'espace de travail.

Le code est simple — regardez la fonction principale :

```python
gps_goal_node = GpsGoalNode()  # create the object
lat, long = DMS_to_decimal_format(lat, long)  # parse the coordinates: from the command line and from the topic
gps_goal_node.do_gps_goal(lat, long, roll=roll, pitch=pitch, yaw=yaw)
```

La fonction `do_gps_goal` :

```python
def do_gps_goal(self, goal_lat, goal_long, z=0, yaw=0, roll=0, pitch=0):
    # Calculate goal x and y in the frame_id given the frame's origin GPS and a goal GPS location
    # convert lat/long into xy in the Nav2 map
    x, y = calc_goal(self.origin_lat, self.origin_long, goal_lat, goal_long)
    print("Goal x: ", x)
    print("Goal y: ", y)
    self.publish_goal(x=x, y=y, z=z, yaw=yaw, roll=roll, pitch=pitch)
```

`calc_goal` calcule les valeurs xy à partir des coordonnées d'origine et d'objectif. `publish_goal` empaquette les valeurs xy dans un message `NavigateToPose.Goal()` et l'envoie via une action.

## Test avec un faux serveur Nav2

Ouvrez un terminal :

```
cd ~/GPS_ROS2
```

```
ros2 launch gps_goal gps_goal_demo.launch.py
```

Ouvrez un nouveau terminal :

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
