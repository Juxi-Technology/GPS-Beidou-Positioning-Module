#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix


class GPSListener(Node):
    def __init__(self):
        super().__init__('gps_subscriber')
        self.subscription = self.create_subscription(
            NavSatFix,
            '/fix',
            self.gps_callback,
            10
        )

    def gps_callback(self, msg):
        self.get_logger().info("latitude:%.6f, longitude:%.6f, altitude:%.6f" %
                              (msg.latitude, msg.longitude, msg.altitude))


def main(args=None):
    rclpy.init(args=args)
    node = GPSListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
