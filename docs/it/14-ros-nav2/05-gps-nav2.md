[English](../../en/14-ros-nav2/05-gps-nav2.md) | [Deutsch](../../de/14-ros-nav2/05-gps-nav2.md) | [Español](../../es/14-ros-nav2/05-gps-nav2.md) | [Français](../../fr/14-ros-nav2/05-gps-nav2.md) | Italiano | [日本語](../../ja/14-ros-nav2/05-gps-nav2.md) | [한국어](../../ko/14-ros-nav2/05-gps-nav2.md) | [Português (BR)](../../pt-br/14-ros-nav2/05-gps-nav2.md) | [Português (PT)](../../pt-pt/14-ros-nav2/05-gps-nav2.md) | [简体中文](../../zh-hans/14-ros-nav2/05-gps-nav2.md) | [繁體中文](../../zh-hant/14-ros-nav2/05-gps-nav2.md)

### Navigazione GPS e Nav2

**Per navigare verso una data latitudine/longitudine con Nav2 non si può inviare il goal direttamente — le coordinate devono prima essere convertite in valori xy di goal per Nav2. Questa sezione spiega tale conversione.**

#### 1. Esecuzione

Nav2 deve essere già in esecuzione. È possibile caricare una mappa vuota, ma le coordinate di origine e di goal devono trovarsi all'interno di quella mappa — altrimenti il programma avvisa `The goal sent to the planner is off the global costmap. Planning will always fail to this goal`, il che significa che il planner non lo raggiungerà mai. L'avvio di Nav2 non è trattato qui; presumiamo che sia già attivo.

Con Nav2 in esecuzione, in un terminale:

```
ros2 launch gps_goal gps_goal.launch.py
```

- Fornire la latitudine/longitudine di origine (dove sono?)

```
ros2 topic pub /local_xy_origin geometry_msgs/msg/PoseStamped "{header: {frame_id: 'map'}, pose: {position: {x: 43.658, y: -79.379}}}" -1
```

Questo pubblica sul topic `/local_xy_origin`. I valori x e y sono esempi e vanno impostati in base alla propria situazione.

Dopo l'esecuzione il terminale stampa `Received origin: lat -79.379, long 43.658`.

![origine](../../en/14-ros-nav2/images/1.png)

- Fornire la latitudine/longitudine di goal (dove sto andando?)

```
ros2 topic pub /gps_goal_fix sensor_msgs/msg/NavSatFix "{latitude: 2.548, longitude: 11.06455}" -1
```

Questo pubblica su `/gps_goal_fix`. Anche queste coordinate sono esempi.

Dopo l'esecuzione il terminale stampa:

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

![output del goal](../../en/14-ros-nav2/images/2.png)

Dall'output: la distanza tra i due punti è **9284767.487 m** (poiché le coordinate fornite differiscono enormemente) e l'azimut è **-32.818°**. Il valore xy di goal convertito è (7802896.906, -5032067.881) — chiaramente molto al di fuori della mappa, quindi la pianificazione non potrà mai raggiungerlo. Ecco perché conta la nota precedente: **le coordinate di origine e di goal devono trovarsi all'interno della mappa.** Una volta calcolati, i valori xy vengono impacchettati e inviati a Nav2 per la pianificazione.

#### 2. Informazioni sul sorgente

Percorso del sorgente: `src/gps_goal/gps_goal/gps_goal.py` nel workspace.

Il codice è semplice — guarda la funzione main:

```python
gps_goal_node = GpsGoalNode()  # create the object
lat, long = DMS_to_decimal_format(lat, long)  # parse the coordinates: from the command line and from the topic
gps_goal_node.do_gps_goal(lat, long, roll=roll, pitch=pitch, yaw=yaw)
```

La funzione `do_gps_goal`:

```python
def do_gps_goal(self, goal_lat, goal_long, z=0, yaw=0, roll=0, pitch=0):
    # Calculate goal x and y in the frame_id given the frame's origin GPS and a goal GPS location
    # convert lat/long into xy in the Nav2 map
    x, y = calc_goal(self.origin_lat, self.origin_long, goal_lat, goal_long)
    print("Goal x: ", x)
    print("Goal y: ", y)
    self.publish_goal(x=x, y=y, z=z, yaw=yaw, roll=roll, pitch=pitch)
```

`calc_goal` calcola i valori xy dalle coordinate di origine e di goal. `publish_goal` impacchetta i valori xy come messaggio `NavigateToPose.Goal()` e li invia tramite un'action.

## Test con un server Nav2 finto

Aprire un terminale:

```
cd ~/GPS_ROS2
```

```
ros2 launch gps_goal gps_goal_demo.launch.py
```

Aprire un nuovo terminale:

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
