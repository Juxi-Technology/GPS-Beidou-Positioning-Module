#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import PoseStamped, Quaternion
from nav2_msgs.action import NavigateToPose

import math
from geographiclib.geodesic import Geodesic
from tf_transformations import quaternion_from_euler


def DMS_to_decimal_format(lat, long):
    if ',' in str(lat):
        degrees, minutes, seconds = str(lat).split(',')
        degrees, minutes, seconds = float(degrees), float(minutes), float(seconds)
        if lat[0] == '-':
            minutes = -minutes
            seconds = -seconds
        lat = degrees + minutes/60 + seconds/3600
    if ',' in str(long):
        degrees, minutes, seconds = str(long).split(',')
        degrees, minutes, seconds = float(degrees), float(minutes), float(seconds)
        if long[0] == '-':
            minutes = -minutes
            seconds = -seconds
        long = degrees + minutes/60 + seconds/3600

    lat = float(lat)
    long = float(long)
    return lat, long


def calc_goal(origin_lat, origin_long, goal_lat, goal_long):
    geod = Geodesic.WGS84
    g = geod.Inverse(origin_lat, origin_long, goal_lat, goal_long)
    distance = g['s12']
    azimuth = g['azi1']

    azimuth = math.radians(azimuth)
    x = math.cos(azimuth) * distance
    y = math.sin(azimuth) * distance

    return x, y


class GpsGoal(Node):
    def __init__(self):
        super().__init__('gps_goal')

        self.declare_parameter('frame_id', 'map')
        self.declare_parameter('dry_run', True)  # 调试模式：只打印，不发送
        self.frame_id = self.get_parameter('frame_id').value
        self.dry_run = self.get_parameter('dry_run').value

        self.origin_lat = None
        self.origin_long = None
        self.origin_received = False

        qos_profile = QoSProfile(
            depth=10,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL
        )

        if self.dry_run:
            self.get_logger().info('=' * 50)
            self.get_logger().info('DRY RUN MODE - Coordinate conversion only')
            self.get_logger().info('Goal will NOT be sent to Nav2')
            self.get_logger().info('=' * 50)
            self.nav_to_pose_client = None
        else:
            self.nav_to_pose_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
            while not self.nav_to_pose_client.wait_for_server(timeout_sec=1.0):
                self.get_logger().info('Waiting for NavigateToPose action server...')

        self.origin_sub = self.create_subscription(
            PoseStamped,
            '/local_xy_origin',
            self.origin_callback,
            qos_profile
        )

        self.gps_goal_pose_sub = self.create_subscription(
            PoseStamped,
            'gps_goal_pose',
            self.gps_goal_pose_callback,
            10
        )

        self.gps_goal_fix_sub = self.create_subscription(
            NavSatFix,
            'gps_goal_fix',
            self.gps_goal_fix_callback,
            10
        )

        self.get_logger().info('GPS Goal node initialized. Waiting for origin...')

    def origin_callback(self, msg):
        self.origin_lat = msg.pose.position.y
        self.origin_long = msg.pose.position.x
        self.origin_received = True
        self.get_logger().info(f'Received origin: lat {self.origin_lat:.6f}, long {self.origin_long:.6f}')

    def gps_goal_pose_callback(self, data):
        if not self.origin_received:
            self.get_logger().warn('No origin received yet. Cannot compute goal.')
            return

        lat = data.pose.position.y
        long = data.pose.position.x
        self.do_gps_goal(lat, long)

    def gps_goal_fix_callback(self, data):
        if not self.origin_received:
            self.get_logger().warn('No origin received yet. Cannot compute goal.')
            return

        self.do_gps_goal(data.latitude, data.longitude)

    def do_gps_goal(self, goal_lat, goal_long, z=0.0, yaw=0.0, roll=0.0, pitch=0.0):
        x, y = calc_goal(self.origin_lat, self.origin_long, goal_lat, goal_long)
        self.get_logger().info(f'Goal x: {x:.3f}, y: {y:.3f}')
        self.publish_goal(x=x, y=y, z=float(z), yaw=float(yaw), roll=float(roll), pitch=float(pitch))

    def publish_goal(self, x=0.0, y=0.0, z=0.0, yaw=0.0, roll=0.0, pitch=0.0):
        goal_msg = NavigateToPose.Goal()
        
        pose = PoseStamped()
        pose.header.frame_id = self.frame_id
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.position.x = float(x)
        pose.pose.position.y = float(y)
        pose.pose.position.z = float(z)

        quaternion = quaternion_from_euler(roll, pitch, yaw)
        pose.pose.orientation = Quaternion(
            x=quaternion[0],
            y=quaternion[1],
            z=quaternion[2],
            w=quaternion[3]
        )

        goal_msg.pose = pose

        self.get_logger().info(f'Executing Nav2 goal to position (x,y) {x:.3f}, {y:.3f}, with {yaw:.3f} radians yaw.')

        if self.dry_run:
            self.get_logger().info('=' * 50)
            self.get_logger().info('DRY RUN - Coordinate conversion result:')
            self.get_logger().info(f'  Origin GPS: lat={self.origin_lat:.6f}, lon={self.origin_long:.6f}')
            self.get_logger().info(f'  Goal Local: x={x:.3f}m, y={y:.3f}m')
            self.get_logger().info(f'  Goal Orientation: roll={roll:.3f}, pitch={pitch:.3f}, yaw={yaw:.3f} rad')
            self.get_logger().info(f'  Quaternion: [{quaternion[0]:.4f}, {quaternion[1]:.4f}, {quaternion[2]:.4f}, {quaternion[3]:.4f}]')
            self.get_logger().info('=' * 50)
            self.get_logger().info('Set dry_run:=False to actually send goal to Nav2')
            return

        send_goal_future = self.nav_to_pose_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        send_goal_future.add_done_callback(self.goal_response_callback)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(
            f'Distance remaining: {feedback.distance_remaining:.2f} meters',
            throttle_duration_sec=1.0
        )

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Goal rejected by action server')
            return

        self.get_logger().info('Goal accepted by the action server')
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        status = future.result().status

        if status == 4:
            self.get_logger().info('Navigation succeeded!')
        else:
            self.get_logger().warn(f'Navigation failed with status: {status}')


def main(args=None):
    rclpy.init(args=args)

    gps_goal = GpsGoal()

    try:
        rclpy.spin(gps_goal)
    except KeyboardInterrupt:
        pass
    finally:
        gps_goal.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
