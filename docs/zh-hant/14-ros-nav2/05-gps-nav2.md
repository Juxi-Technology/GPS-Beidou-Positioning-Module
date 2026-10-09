[English](../../en/14-ros-nav2/05-gps-nav2.md) | [Deutsch](../../de/14-ros-nav2/05-gps-nav2.md) | [Español](../../es/14-ros-nav2/05-gps-nav2.md) | [Français](../../fr/14-ros-nav2/05-gps-nav2.md) | [Italiano](../../it/14-ros-nav2/05-gps-nav2.md) | [日本語](../../ja/14-ros-nav2/05-gps-nav2.md) | [한국어](../../ko/14-ros-nav2/05-gps-nav2.md) | [Português (BR)](../../pt-br/14-ros-nav2/05-gps-nav2.md) | [Português (PT)](../../pt-pt/14-ros-nav2/05-gps-nav2.md) | [简体中文](../../zh-hans/14-ros-nav2/05-gps-nav2.md) | 繁體中文

### GPS與Nav2導航

**要想給定一個經緯度，然後利用Nav2導航到該點，直接給定目標點是不行的，所以需要把經緯度轉換成Nav2目標點的xy資料，本節內容就說明如何實現資料轉換。**

#### 1、啟動步驟

啟動前，需要成功把Nav2打開，地圖可以匯入一張空白的地圖，得要確保需要到的點的經緯度是在該地圖上的，不然程式會給出警告說“The goal sent to the planner is off the global costmap. Planning will always fail to this goal，”，這就表示路徑規劃會到不了這個地方。這裡不做執行Nav2的程式，預設是成功打開Nav2的。

成功打開Nav2後，終端機輸入，

```
ros2 launch gps_goal gps_goal.launch.py
```

- 給定初始位置經緯度（我在哪？）

```
ros2 topic pub /local_xy_origin geometry_msgs/msg/PoseStamped "{header: {frame_id: 'map'}, pose: {position: {x: 43.658, y: -79.379}}}" -1
```

這裡就是發布一條訊息，話題名字是“/local_xy_origin”，後邊的資料x，y資料是參考值，需要按照實際情況賦值，

執行後，終端機會列印出“Received origin: lat -79.379, long 43.658”，

![step-1-publish-origin](../../en/14-ros-nav2/images/1.png)

- 給定目標點經緯度（我去哪？）

```
ros2 topic pub /gps_goal_fix sensor_msgs/msg/NavSatFix "{latitude: 2.548, longitude: 11.06455}" -1
```

這裡發布了/gps_goal_fix話題訊息的資料，裡邊的經緯度資料也是僅供參考的，需要按照實際情況給的值。

執行後，終端機會列印如下訊息，

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

![step-2-goal-output](../../en/14-ros-nav2/images/2.png)

列印訊息我們知道，計算到兩個點的距離是**9284767.487 公尺**（這是因為我們給的經緯度相差太大），方位角是**-32.818度**；後面轉換後，就列印出了（7802896.906, -5032067.881）這是在Nav2地圖中的目標點的xy值，這個值明顯的超過我們的地圖的範圍的，所以路徑規劃是不可能到這裡的。這就是前邊為啥提到了，**需要保證原點和目標點的經緯度必須是在地圖中。**計算出xy值後，就把資料打包，發送給Nav2那邊做路徑規劃。

#### 2、程式原始碼說明

程式碼路徑：工作空間src/gps_goal/gps_goal/gps_goal.py

程式碼很簡單，直接看main函式，

```python
gps_goal_node = GpsGoalNode()  # 创建对象
lat, long = DMS_to_decimal_format(lat, long)  # 解析经纬度，这部分主要是解析命令行发送过去的数据和话题发送过去的经纬度
gps_goal_node.do_gps_goal(lat, long, roll=roll, pitch=pitch, yaw=yaw)
```

do_gps_goal函式

```python
def do_gps_goal(self, goal_lat, goal_long, z=0, yaw=0, roll=0, pitch=0):
    # Calculate goal x and y in the frame_id given the frame's origin GPS and a goal GPS location
    # 转换经纬度成Nav2导航地图中的xy值
    x, y = calc_goal(self.origin_lat, self.origin_long, goal_lat, goal_long)
    print("Goal x: ", x)
    print("Goal y: ", y)
    self.publish_goal(x=x, y=y, z=z, yaw=yaw, roll=roll, pitch=pitch)
```

calc_goal函式，根據原點經緯度和目標點經緯度，算出xy值

publish_goal函式，把xy值打包成NavigateToPose.Goal()類型的資料，透過action發送出去





## **假 Nav2 伺服器測試**

打開終端機

```
cd ~/GPS_ROS2
```

```
ros2 launch gps_goal gps_goal_demo.launch.py
```



打開新終端機

```
# 设置原点
ros2 topic pub --once /local_xy_origin geometry_msgs/msg/PoseStamped "{
  header: {frame_id: 'map'},
  pose: {position: {x: 0.0, y: 0.0}}
}"
```

```
# 设置目标点（向北走5米）
ros2 topic pub --once /gps_goal_fix sensor_msgs/msg/NavSatFix "{
  latitude: 0.000045, longitude: 0.0
}"
```

