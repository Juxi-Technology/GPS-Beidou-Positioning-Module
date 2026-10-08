#!/usr/bin/env python3
import serial
import sys

import rclpy
from rclpy.node import Node

from nmea_navsat_driver.driver import RosNMEADriver


class NMEASerialDriver(Node):
    def __init__(self):
        super().__init__('nmea_serial_driver')

        self.serial_port = self.declare_parameter('port', '/dev/ttyUSB0').value
        self.serial_baud = self.declare_parameter('baud', 9600).value
        self.frame_id = RosNMEADriver.get_frame_id(self)

        self.driver = RosNMEADriver(self)
        self.gps = None

        self.get_logger().info("=" * 50)
        self.get_logger().info("NMEA Serial Driver Starting...")
        self.get_logger().info(f"Serial port: {self.serial_port}")
        self.get_logger().info(f"Baud rate: {self.serial_baud}")
        self.get_logger().info(f"Frame ID: {self.frame_id}")
        self.get_logger().info("=" * 50)

    def run(self):
        try:
            self.get_logger().info(f"Opening serial port: {self.serial_port} @ {self.serial_baud} baud")
            self.gps = serial.Serial(port=self.serial_port, baudrate=self.serial_baud, timeout=2)
            self.get_logger().info("Serial port opened successfully!")
            self.get_logger().info("Waiting for GPS data...")

            line_count = 0
            while rclpy.ok():
                data = self.gps.readline().strip()
                if data:
                    line_count += 1
                    try:
                        data_str = data.decode('ascii', errors='replace')
                        
                        if line_count <= 5:  # 只打印前5行调试
                            self.get_logger().debug(f"Raw data: {data_str}")
                        
                        if line_count == 1:
                            self.get_logger().info("Receiving GPS data!")
                        
                        self.driver.add_sentence(data_str, self.frame_id)
                    except ValueError as e:
                        self.get_logger().warn(
                            "Value error, likely due to missing fields in the NMEA message. "
                            "Error was: %s. Please report this issue at "
                            "github.com/ros-drivers/nmea_navsat_driver, including a bag file with the NMEA "
                            "sentences that caused it." % e)

        except serial.SerialException as ex:
            self.get_logger().fatal(
                f"Could not open serial port: I/O error({ex.errno}): {ex.strerror}")
            self.get_logger().fatal("Please check:")
            self.get_logger().fatal("  1. The device exists: ls -l {self.serial_port}")
            self.get_logger().fatal("  2. You have permission: sudo chmod 666 {self.serial_port}")
            self.get_logger().fatal("  3. The device is not used by another program")
        except Exception as e:
            self.get_logger().fatal(f"Unexpected error: {str(e)}")
        finally:
            if self.gps:
                self.gps.close()
                self.get_logger().info("Serial port closed.")


def main(args=None):
    rclpy.init(args=args)
    node = NMEASerialDriver()
    try:
        node.run()
    except KeyboardInterrupt:
        node.get_logger().info("Received Ctrl+C, shutting down...")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
