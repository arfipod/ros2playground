"""Kinematic simulator: no dynamics, contact solver, GPU or external models."""
import math
import time
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from geometry_msgs.msg import Twist, TransformStamped
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from std_srvs.srv import Trigger
from tf2_ros import TransformBroadcaster
from visualization_msgs.msg import Marker, MarkerArray
from .core import integrate, ray_circle

OBSTACLES = [(2.0, 0.0, 0.45), (-1.5, 1.2, 0.5), (0.5, -2.0, 0.4)]


class Rover(Node):
    def __init__(self):
        super().__init__('rover')
        self.x = self.y = self.yaw = self.v = self.w = 0.0
        self.last_command = 0.0
        self.last_tick = time.monotonic()
        self.odom_pub = self.create_publisher(Odometry, 'odom', 10)
        self.scan_pub = self.create_publisher(LaserScan, 'scan', qos_profile_sensor_data)
        self.marker_pub = self.create_publisher(MarkerArray, 'scene', 10)
        self.tf = TransformBroadcaster(self)
        self.command_sub = self.create_subscription(Twist, 'cmd_vel', self.command, 10)
        self.reset_srv = self.create_service(Trigger, 'reset_world', self.reset)
        self.timer = self.create_timer(0.1, self.tick)

    def command(self, msg):
        v, w = msg.linear.x, msg.angular.z
        if math.isfinite(v) and math.isfinite(w):
            self.v, self.w = max(-0.35, min(0.35, v)), max(-1.0, min(1.0, w))
            self.last_command = time.monotonic()
        else:
            self.v = self.w = 0.0

    def reset(self, _request, response):
        self.x = self.y = self.yaw = self.v = self.w = 0.0
        self.last_command = 0.0
        response.success = True
        response.message = 'Pose reset. Set mode OFF before resetting.'
        return response

    def tick(self):
        now = time.monotonic()
        dt = min(0.2, now - self.last_tick)
        self.last_tick = now
        if now - self.last_command > 0.5:
            self.v = self.w = 0.0
        self.x, self.y, self.yaw = integrate(self.x, self.y, self.yaw, self.v, self.w, dt)
        stamp = self.get_clock().now().to_msg()
        odom = Odometry()
        odom.header.stamp, odom.header.frame_id, odom.child_frame_id = stamp, 'odom', 'base_link'
        odom.pose.pose.position.x, odom.pose.pose.position.y = self.x, self.y
        odom.pose.pose.orientation.z = math.sin(self.yaw / 2)
        odom.pose.pose.orientation.w = math.cos(self.yaw / 2)
        odom.twist.twist.linear.x, odom.twist.twist.angular.z = self.v, self.w
        self.odom_pub.publish(odom)
        transform = TransformStamped()
        transform.header, transform.child_frame_id = odom.header, 'base_link'
        transform.transform.translation.x, transform.transform.translation.y = self.x, self.y
        transform.transform.rotation = odom.pose.pose.orientation
        self.tf.sendTransform(transform)
        scan = LaserScan()
        scan.header.stamp, scan.header.frame_id = stamp, 'base_link'
        scan.angle_min, scan.angle_max = -math.pi, math.pi
        scan.angle_increment = 2 * math.pi / 180
        scan.range_min, scan.range_max, scan.scan_time = 0.0, 6.0, 0.1
        scan.ranges = [float(min(ray_circle(self.x, self.y, self.yaw + scan.angle_min +
                            i * scan.angle_increment, o) for o in OBSTACLES)) for i in range(181)]
        self.scan_pub.publish(scan)
        scene = MarkerArray()
        for i, (x, y, radius) in enumerate([(self.x, self.y, 0.18)] + OBSTACLES):
            marker = Marker()
            marker.header.stamp, marker.header.frame_id = stamp, 'odom'
            marker.ns, marker.id, marker.action = 'course', i, Marker.ADD
            marker.type = Marker.CUBE if i == 0 else Marker.CYLINDER
            marker.pose.position.x, marker.pose.position.y, marker.pose.position.z = x, y, 0.15
            marker.pose.orientation.w = 1.0
            if i == 0:
                marker.pose.orientation.z = math.sin(self.yaw / 2)
                marker.pose.orientation.w = math.cos(self.yaw / 2)
            marker.scale.x = marker.scale.y = radius * 2
            marker.scale.z, marker.color.a = 0.3, 1.0
            marker.color.g = 0.8 if i == 0 else 0.25
            marker.color.r = 0.1 if i == 0 else 0.8
            scene.markers.append(marker)
        self.marker_pub.publish(scene)


def main(args=None):
    rclpy.init(args=args)
    node = Rover()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
