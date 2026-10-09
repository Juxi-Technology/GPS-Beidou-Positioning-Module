[English](../../en/14-ros-nav2/05-gps-nav2.md) | [Deutsch](../../de/14-ros-nav2/05-gps-nav2.md) | [Español](../../es/14-ros-nav2/05-gps-nav2.md) | [Français](../../fr/14-ros-nav2/05-gps-nav2.md) | [Italiano](../../it/14-ros-nav2/05-gps-nav2.md) | 日本語 | [한국어](../../ko/14-ros-nav2/05-gps-nav2.md) | [Português (BR)](../../pt-br/14-ros-nav2/05-gps-nav2.md) | [Português (PT)](../../pt-pt/14-ros-nav2/05-gps-nav2.md) | [简体中文](../../zh-hans/14-ros-nav2/05-gps-nav2.md) | [繁體中文](../../zh-hant/14-ros-nav2/05-gps-nav2.md)

### GPS と Nav2 ナビゲーション

**Nav2 で指定した緯度・経度へナビゲーションするには、ゴールを直接送信することはできません。まず座標を Nav2 のゴール xy 値に変換する必要があります。本セクションではその変換について説明します。**

#### 1. 実行方法

Nav2 がすでに起動している必要があります。空のマップをロードしてもかまいませんが、原点とゴールの座標がそのマップ内に収まっていなければなりません。そうでない場合、プログラムは `The goal sent to the planner is off the global costmap. Planning will always fail to this goal` と警告します。これは、プランナーがそのゴールに決して到達できないことを意味します。Nav2 の起動についてはここでは扱いません。すでに起動しているものとします。

Nav2 を起動した状態で、ターミナルで：

```
ros2 launch gps_goal gps_goal.launch.py
```

- 原点の緯度・経度を指定します（自分はどこにいるか？）

```
ros2 topic pub /local_xy_origin geometry_msgs/msg/PoseStamped "{header: {frame_id: 'map'}, pose: {position: {x: 43.658, y: -79.379}}}" -1
```

これは `/local_xy_origin` トピックに配信します。x と y の値は例であり、状況に合わせて設定してください。

実行後、ターミナルは `Received origin: lat -79.379, long 43.658` と出力します。

![原点](../../en/14-ros-nav2/images/1.png)

- ゴールの緯度・経度を指定します（どこへ行くか？）

```
ros2 topic pub /gps_goal_fix sensor_msgs/msg/NavSatFix "{latitude: 2.548, longitude: 11.06455}" -1
```

これは `/gps_goal_fix` に配信します。これらの座標も例です。

実行後、ターミナルは次のように出力します：

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

![ゴール出力](../../en/14-ros-nav2/images/2.png)

この出力から、2 点間の距離は **9284767.487 m**（指定した座標が大きく離れているため）、方位角は **-32.818°** であることがわかります。変換後のゴール xy 値は (7802896.906, -5032067.881) で、明らかにマップの外側にあるため、プランナーは決して到達できません。だからこそ先ほどの注意が重要です。**原点とゴールの座標はマップ内に収まっていなければなりません。** xy 値が計算されると、それらはまとめられて Nav2 に送信され、プランニングが行われます。

#### 2. ソースについて

ソースパス：ワークスペース内の `src/gps_goal/gps_goal/gps_goal.py`。

コードはシンプルです。main 関数を見てみましょう：

```python
gps_goal_node = GpsGoalNode()  # create the object
lat, long = DMS_to_decimal_format(lat, long)  # parse the coordinates: from the command line and from the topic
gps_goal_node.do_gps_goal(lat, long, roll=roll, pitch=pitch, yaw=yaw)
```

`do_gps_goal` 関数：

```python
def do_gps_goal(self, goal_lat, goal_long, z=0, yaw=0, roll=0, pitch=0):
    # Calculate goal x and y in the frame_id given the frame's origin GPS and a goal GPS location
    # convert lat/long into xy in the Nav2 map
    x, y = calc_goal(self.origin_lat, self.origin_long, goal_lat, goal_long)
    print("Goal x: ", x)
    print("Goal y: ", y)
    self.publish_goal(x=x, y=y, z=z, yaw=yaw, roll=roll, pitch=pitch)
```

`calc_goal` は原点とゴールの座標から xy 値を計算します。`publish_goal` は xy 値を `NavigateToPose.Goal()` メッセージとしてまとめ、アクションで送信します。

## 偽の Nav2 サーバーでのテスト

ターミナルを開きます：

```
cd ~/GPS_ROS2
```

```
ros2 launch gps_goal gps_goal_demo.launch.py
```

新しいターミナルを開きます：

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
