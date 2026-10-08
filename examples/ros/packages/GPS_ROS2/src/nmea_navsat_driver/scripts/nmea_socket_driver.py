#!/usr/bin/env python3
import socket
import sys

import rclpy
from rclpy.node import Node

from nmea_navsat_driver.driver import RosNMEADriver


class NMEASocketDriver(Node):
    def __init__(self):
        super().__init__('nmea_socket_driver')

        self.local_ip = self.declare_parameter('ip', '0.0.0.0').value
        self.local_port = self.declare_parameter('port', 10110).value
        self.buffer_size = self.declare_parameter('buffer_size', 4096).value
        self.timeout = self.declare_parameter('timeout_sec', 2).value

        self.frame_id = RosNMEADriver.get_frame_id(self)
        self.driver = RosNMEADriver(self)

    def run(self):
        while rclpy.ok():
            try:
                socket_ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                socket_.bind((self.local_ip, self.local_port))
                socket_.settimeout(self.timeout)
            except socket.error as exc:
                self.get_logger().error(
                    "Caught exception socket.error when setting up socket: %s" % exc)
                sys.exit(1)

            while rclpy.ok():
                try:
                    data, remote_address = socket_.recvfrom(self.buffer_size)
                    data_list = data.strip().split(b"\n")

                    for data_line in data_list:
                        try:
                            data_str = data_line.decode('ascii', errors='replace')
                            self.driver.add_sentence(data_str, self.frame_id)
                        except ValueError as e:
                            self.get_logger().warn(
                                "Value error, likely due to missing fields in the NMEA message. "
                                "Error was: %s. Please report this issue at "
                                "github.com/ros-drivers/nmea_navsat_driver, including a bag file with the NMEA "
                                "sentences that caused it." % e)

                except socket.error as exc:
                    self.get_logger().error(
                        "Caught exception socket.error during recvfrom: %s" % exc)
                    socket_.close()
                    break

            socket_.close()


def main(args=None):
    rclpy.init(args=args)
    node = NMEASocketDriver()
    try:
        node.run()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
