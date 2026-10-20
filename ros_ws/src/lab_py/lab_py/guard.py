"""Exercise gate, not a certified safety controller for physical robots."""
import time
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_srvs.srv import SetBool
from .core import front_distance, guarded_command


class Guard(Node):
    def __init__(self):
        super().__init__('guard')
        self.v = self.w = 0.0
        self.command_stamp = self.scan_stamp = 0.0
        self.distance = None
        self.emergency = False
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.command_sub = self.create_subscription(Twist, 'cmd_vel_raw', self.command, 10)
        self.scan_sub = self.create_subscription(LaserScan, 'scan', self.scan, qos_profile_sensor_data)
        self.estop_srv = self.create_service(SetBool, 'emergency_stop', self.estop)
        self.timer = self.create_timer(0.05, self.tick)

    def command(self, msg):
        self.v, self.w, self.command_stamp = msg.linear.x, msg.angular.z, time.monotonic()

    def scan(self, msg):
        self.distance = front_distance(msg.ranges, msg.angle_min, msg.angle_increment)
        self.scan_stamp = time.monotonic()

    def estop(self, request, response):
        self.emergency = request.data
        self.command_stamp = 0.0  # Require a fresh command after changing the latch.
        self.tick()
        response.success = True
        response.message = 'Emergency latched' if self.emergency else 'Emergency released'
        return response

    def tick(self):
        now = time.monotonic()
        v, w = guarded_command(self.v, self.w, now - self.command_stamp,
                               now - self.scan_stamp, self.distance, self.emergency)
        msg = Twist()
        msg.linear.x, msg.angular.z = v, w
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = Guard()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
