[English](05-gps-nav2.md) | 简体中文

### GPS与Nav2导航

**要想给定一个经纬度，然后利用Nav2导航到该点，直接给定目标点是不行的，所以需要把经纬度转换成Nav2目标点的xy数据，本节内容就说明如何实现数据转换。**

#### 1、启动步骤

启动前，需要成功把Nav2打开，地图可以导入一张空白的地图，得要确保需要到的点的经纬度是在该地图上的，不然程序会给出警告说“The goal sent to the planner is off the global costmap. Planning will always fail to this goal，”，这就表示路径规划会到不了这个地方。这里不做运行Nav2的程序，默认是成功打开Nav2的。

成功打开Nav2后，终端输入，

```
ros2 launch gps_goal gps_goal.launch.py
```

- 给定初始位置经纬度（我在哪？）

```
ros2 topic pub /local_xy_origin geometry_msgs/msg/PoseStamped "{header: {frame_id: 'map'}, pose: {position: {x: 43.658, y: -79.379}}}" -1
```

这里就是发布一条消息，话题名字是“/local_xy_origin”，后边的数据x，y数据是参考值，需要按照实际情况赋值，

运行后，终端会打印出“Received origin: lat -79.379, long 43.658”，

![step-1-publish-origin](1.png)

- 给定目标点经纬度（我去哪？）

```
ros2 topic pub /gps_goal_fix sensor_msgs/msg/NavSatFix "{latitude: 2.548, longitude: 11.06455}" -1
```

这里发布了/gps_goal_fix话题消息的数据，里边的经纬度数据也是仅供参考的，需要按照实际情况给的值。

运行后，终端会打印如下消息，

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

![step-2-goal-output](2.png)

打印消息我们知道，计算到两个点的距离是**9284767.487 米**（这是因为我们给的经纬度相差太大），方位角是**-32.818度**；后面转换后，就打印出了（7802896.906, -5032067.881）这是在Nav2地图中的目标点的xy值，这个值明显的超过我们的地图的范围的，所以路径规划是不可能到这里的。这就是前边为啥提到了，**需要保证原点和目标点的经纬度必须是在地图中。**计算出xy值后，就把数据打包，发送给Nav2那边做路径规划。

#### 2、程序源码说明

代码路径：工作空间src/gps_goal/gps_goal/gps_goal.py

代码很简单，直接看main函数，

```python
gps_goal_node = GpsGoalNode()  # 创建对象
lat, long = DMS_to_decimal_format(lat, long)  # 解析经纬度，这部分主要是解析命令行发送过去的数据和话题发送过去的经纬度
gps_goal_node.do_gps_goal(lat, long, roll=roll, pitch=pitch, yaw=yaw)
```

do_gps_goal函数

```python
def do_gps_goal(self, goal_lat, goal_long, z=0, yaw=0, roll=0, pitch=0):
    # Calculate goal x and y in the frame_id given the frame's origin GPS and a goal GPS location
    # 转换经纬度成Nav2导航地图中的xy值
    x, y = calc_goal(self.origin_lat, self.origin_long, goal_lat, goal_long)
    print("Goal x: ", x)
    print("Goal y: ", y)
    self.publish_goal(x=x, y=y, z=z, yaw=yaw, roll=roll, pitch=pitch)
```

calc_goal函数，根据原点经纬度和目标点经纬度，算出xy值

publish_goal函数，把xy值打包成NavigateToPose.Goal()类型的数据，通过action发送出去





## **假 Nav2 服务器测试**

打开终端

```
cd ~/GPS_ROS2
```

```
ros2 launch gps_goal gps_goal_demo.launch.py
```



打开新终端

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

