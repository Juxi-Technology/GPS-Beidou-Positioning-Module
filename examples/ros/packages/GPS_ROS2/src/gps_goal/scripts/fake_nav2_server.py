#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse
from nav2_msgs.action import NavigateToPose


class FakeNav2Server(Node):
    def __init__(self):
        super().__init__('fake_nav2_server')
        
        self._action_server = ActionServer(
            self,
            NavigateToPose,
            'navigate_to_pose',
            self.execute_callback,
            goal_callback=self.goal_callback
        )
        
        self.get_logger().info('=' * 50)
        self.get_logger().info('Fake Nav2 Action Server Started!')
        self.get_logger().info('Action: /navigate_to_pose')
        self.get_logger().info('This server will ACCEPT all goals.')
        self.get_logger().info('=' * 50)

    def goal_callback(self, goal_request):
        self.get_logger().info('=' * 50)
        self.get_logger().info('Received NEW GOAL!')
        self.get_logger().info(f'  Position: x={goal_request.pose.pose.position.x:.3f}, '
                              f'y={goal_request.pose.pose.position.y:.3f}')
        self.get_logger().info(f'  Frame: {goal_request.pose.header.frame_id}')
        self.get_logger().info('Goal ACCEPTED!')
        self.get_logger().info('=' * 50)
        return GoalResponse.ACCEPT

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal... (fake navigation)')
        
        # 假装导航中...
        import time
        for i in range(5):
            self.get_logger().info(f'  Navigating... {i+1}/5')
            time.sleep(0.5)
        
        # 报告成功
        goal_handle.succeed()
        self.get_logger().info('Goal SUCCEEDED!')
        
        result = NavigateToPose.Result()
        return result


def main(args=None):
    rclpy.init(args=args)
    node = FakeNav2Server()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down...')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
