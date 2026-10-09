[English](../../en/14-ros-nav2/05-gps-nav2.md) | [Deutsch](../../de/14-ros-nav2/05-gps-nav2.md) | [Español](../../es/14-ros-nav2/05-gps-nav2.md) | [Français](../../fr/14-ros-nav2/05-gps-nav2.md) | [Italiano](../../it/14-ros-nav2/05-gps-nav2.md) | [日本語](../../ja/14-ros-nav2/05-gps-nav2.md) | 한국어 | [Português (BR)](../../pt-br/14-ros-nav2/05-gps-nav2.md) | [Português (PT)](../../pt-pt/14-ros-nav2/05-gps-nav2.md) | [简体中文](../../zh-hans/14-ros-nav2/05-gps-nav2.md) | [繁體中文](../../zh-hant/14-ros-nav2/05-gps-nav2.md)

### GPS와 Nav2 내비게이션

**Nav2로 지정한 위도/경도로 이동하려면 goal을 직접 보낼 수 없습니다. 좌표를 먼저 Nav2 goal의 xy 값으로 변환해야 합니다. 이 섹션에서는 그 변환을 설명합니다.**

#### 1. 실행

Nav2가 이미 실행 중이어야 합니다. 빈 지도를 로드해도 되지만, 원점과 goal 좌표가 그 지도 안에 있어야 합니다. 그렇지 않으면 프로그램이 `The goal sent to the planner is off the global costmap. Planning will always fail to this goal`이라는 경고를 출력하며, 이는 플래너가 결코 그 goal에 도달하지 못한다는 뜻입니다. Nav2 시작은 여기에서 다루지 않으며, 이미 실행 중이라고 가정합니다.

Nav2가 실행 중인 상태에서 터미널에서:

```
ros2 launch gps_goal gps_goal.launch.py
```

- 원점 위도/경도 입력 (나는 어디에 있는가?)

```
ros2 topic pub /local_xy_origin geometry_msgs/msg/PoseStamped "{header: {frame_id: 'map'}, pose: {position: {x: 43.658, y: -79.379}}}" -1
```

이는 `/local_xy_origin` 토픽으로 발행합니다. x와 y 값은 예시이며, 상황에 맞게 설정해야 합니다.

실행하면 터미널에 `Received origin: lat -79.379, long 43.658`이 출력됩니다.

![원점](../../en/14-ros-nav2/images/1.png)

- goal 위도/경도 입력 (나는 어디로 가는가?)

```
ros2 topic pub /gps_goal_fix sensor_msgs/msg/NavSatFix "{latitude: 2.548, longitude: 11.06455}" -1
```

이는 `/gps_goal_fix`로 발행합니다. 이 좌표 역시 예시입니다.

실행하면 터미널에 출력됩니다:

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

![goal 출력](../../en/14-ros-nav2/images/2.png)

출력에서: 두 점 사이의 거리는 **9284767.487 m**이며(주어진 좌표가 매우 크게 다르기 때문), 방위각은 **-32.818°**입니다. 변환된 goal xy 값은 (7802896.906, -5032067.881)로, 지도 범위를 크게 벗어나므로 플래닝이 결코 도달할 수 없습니다. 그래서 앞의 주의 사항이 중요합니다: **원점과 goal 좌표는 반드시 지도 안에 있어야 합니다.** xy 값이 계산되면 패키징되어 Nav2로 전송되어 플래닝에 사용됩니다.

#### 2. 소스에 대한 설명

소스 경로: 워크스페이스의 `src/gps_goal/gps_goal/gps_goal.py`.

코드는 단순합니다. main 함수를 보십시오:

```python
gps_goal_node = GpsGoalNode()  # create the object
lat, long = DMS_to_decimal_format(lat, long)  # parse the coordinates: from the command line and from the topic
gps_goal_node.do_gps_goal(lat, long, roll=roll, pitch=pitch, yaw=yaw)
```

`do_gps_goal` 함수:

```python
def do_gps_goal(self, goal_lat, goal_long, z=0, yaw=0, roll=0, pitch=0):
    # Calculate goal x and y in the frame_id given the frame's origin GPS and a goal GPS location
    # convert lat/long into xy in the Nav2 map
    x, y = calc_goal(self.origin_lat, self.origin_long, goal_lat, goal_long)
    print("Goal x: ", x)
    print("Goal y: ", y)
    self.publish_goal(x=x, y=y, z=z, yaw=yaw, roll=roll, pitch=pitch)
```

`calc_goal`은 원점과 goal 좌표로부터 xy 값을 계산합니다. `publish_goal`은 xy 값을 `NavigateToPose.Goal()` 메시지로 패키징하여 액션으로 전송합니다.

## 가상 Nav2 서버로 테스트

터미널을 엽니다:

```
cd ~/GPS_ROS2
```

```
ros2 launch gps_goal gps_goal_demo.launch.py
```

새 터미널을 엽니다:

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
