#!/usr/bin/env python3
"""Standalone action client: python3 ejemplos/rotate_action.py [--cancel]."""
import sys
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from turtlesim.action import RotateAbsolute


def main():
    cancel = '--cancel' in sys.argv
    rclpy.init(args=[])
    node = Node('rotate_client')
    client = ActionClient(node, RotateAbsolute, '/turtle1/rotate_absolute')
    try:
        if not client.wait_for_server(timeout_sec=5):
            raise RuntimeError('Start ros2 run turtlesim turtlesim_node first')
        goal = RotateAbsolute.Goal()
        goal.theta = 3.0
        sent = client.send_goal_async(goal, feedback_callback=lambda feedback:
                                     node.get_logger().info(f'remaining={feedback.feedback.remaining:.2f} rad'))
        rclpy.spin_until_future_complete(node, sent, timeout_sec=5)
        if not sent.done() or sent.result() is None or not sent.result().accepted:
            raise RuntimeError('Goal timed out or rejected')
        handle = sent.result()
        result = handle.get_result_async()
        if cancel:
            def cancel_once():
                timer.cancel()
                handle.cancel_goal_async()
            timer = node.create_timer(0.5, cancel_once)
        rclpy.spin_until_future_complete(node, result, timeout_sec=20)
        if not result.done():
            raise RuntimeError('Action result timed out')
        print(f'status={result.result().status}; result={result.result().result}')
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
