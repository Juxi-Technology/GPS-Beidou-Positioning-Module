#!/usr/bin/env python3
from nmea_msgs.msg import Sentence
import rclpy
from rclpy.node import Node

from nmea_navsat_driver.driver import RosNMEADriver


class NMEATopicDriver(Node):
    def __init__(self):
        super().__init__('nmea_topic_driver')

        self.driver = RosNMEADriver(self)

        self.subscription = self.create_subscription(
            Sentence,
            'nmea_sentence',
            self.nmea_sentence_callback,
            10
        )

    def nmea_sentence_callback(self, nmea_sentence):
        try:
            self.driver.add_sentence(
                nmea_sentence.sentence,
                frame_id=nmea_sentence.header.frame_id,
                timestamp=nmea_sentence.header.stamp)
        except ValueError as e:
            self.get_logger().warn(
                "Value error, likely due to missing fields in the NMEA message. "
                "Error was: %s. Please report this issue at github.com/ros-drivers/nmea_navsat_driver, "
                "including a bag file with the NMEA sentences that caused it." % e)


def main(args=None):
    rclpy.init(args=args)
    node = NMEATopicDriver()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
