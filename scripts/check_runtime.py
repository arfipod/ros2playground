#!/usr/bin/env python3
"""ROS integration check. Run in a fresh domain, with no course nodes running."""
import os
import signal
import subprocess
import time
from pathlib import Path
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from lab_interfaces.msg import Telemetry
from lab_interfaces.srv import SetMode
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from std_srvs.srv import SetBool


def main():
    log_path = Path('/tmp/ros2-course-runtime.log')
    with log_path.open('w') as log:
        process = subprocess.Popen(['ros2', 'launch', 'lab_py', 'course.launch.py', 'rviz:=false'],
                                   stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        rclpy.init()
        node = Node('course_check')
        received = {}
        def record(key):
            return lambda msg: received.__setitem__(key, (time.monotonic(), msg))
        subscriptions = [
            node.create_subscription(Telemetry, '/telemetry', record('telemetry'), 10),
            node.create_subscription(Odometry, '/odom', record('odom'), 10),
            node.create_subscription(LaserScan, '/scan', record('scan'), qos_profile_sensor_data),
            node.create_subscription(Twist, '/cmd_vel', record('cmd'), 10),
        ]
        def wait_until(predicate, timeout=10):
            deadline = time.monotonic() + timeout
            while time.monotonic() < deadline:
                rclpy.spin_once(node, timeout_sec=0.05)
                if process.poll() is not None:
                    raise RuntimeError(f'Launch exited: {log_path.read_text()}')
                if predicate():
                    return
            raise AssertionError(f'Timeout; received={list(received)}. Log: {log_path}')
        def call(service_type, name, **fields):
            client = node.create_client(service_type, name)
            try:
                if not client.wait_for_service(timeout_sec=10):
                    raise AssertionError(f'Missing {name}')
                request = service_type.Request()
                for key, value in fields.items():
                    setattr(request, key, value)
                future = client.call_async(request)
                wait_until(future.done)
                response = future.result()
                if response is None:
                    raise AssertionError(f'No response {name}')
                return response
            finally:
                node.destroy_client(client)
        try:
            wait_until(lambda: all(k in received for k in ('telemetry', 'odom', 'scan', 'cmd'))
                       and 'monitor' in node.get_node_names(), timeout=30)
            assert not call(SetMode, '/set_mode', mode='INVALID').success
            assert call(SetMode, '/set_mode', mode='PATROL').success
            wait_until(lambda: received['odom'][1].pose.pose.position.x > 0.03)
            assert call(SetBool, '/emergency_stop', data=True).success
            since = time.monotonic()
            wait_until(lambda: received['cmd'][0] > since and received['cmd'][1].linear.x == 0
                       and received['cmd'][1].angular.z == 0)
            deadline = time.monotonic() + 0.6
            while time.monotonic() < deadline:
                rclpy.spin_once(node, timeout_sec=0.05)
                assert received['cmd'][1].linear.x == 0 and received['cmd'][1].angular.z == 0
            assert call(SetMode, '/set_mode', mode='OFF').success
            assert call(SetBool, '/emergency_stop', data=False).success
            print('PASS: Python publisher, C++ node discovered, interfaces, lidar, odometry, mode and emergency gate.')
        finally:
            node.destroy_node()
            if rclpy.ok():
                rclpy.shutdown()
            if process.poll() is None:
                os.killpg(process.pid, signal.SIGINT)
            try:
                process.wait(timeout=8)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()


if __name__ == '__main__':
    main()
