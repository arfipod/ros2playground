"""Copy into lab_py/lab_py/patrol.py to install this worked solution."""
import math
import time
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from rcl_interfaces.msg import SetParametersResult
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
from lab_interfaces.srv import SetMode
from .core import front_distance

BOUNDS = {'speed': (0.0, 0.35), 'turn_speed': (0.0, 1.0), 'obstacle_distance': (0.6, 2.0)}


def valid(name, value):
    low, high = BOUNDS[name]
    return type(value) in (float, int) and math.isfinite(value) and low <= value <= high


class Patrol(Node):
    def __init__(self):
        super().__init__('patrol')
        for name, default in [('speed', 0.2), ('turn_speed', 0.65), ('obstacle_distance', 0.85)]:
            self.declare_parameter(name, default)
            if not valid(name, self.get_parameter(name).value):
                raise ValueError(f'Invalid initial {name}; bounds={BOUNDS[name]}')
        self.add_on_set_parameters_callback(self.validate_parameters)
        self.mode, self.distance, self.scan_stamp = 'OFF', None, 0.0
        self.publisher = self.create_publisher(Twist, 'cmd_vel_raw', 10)
        self.state_publisher = self.create_publisher(String, 'patrol_state', 10)
        self.scan_sub = self.create_subscription(LaserScan, 'scan', self.scan, qos_profile_sensor_data)
        self.mode_srv = self.create_service(SetMode, 'set_mode', self.set_mode)
        self.timer = self.create_timer(0.1, self.tick)

    def validate_parameters(self, params):
        for p in params:
            if p.name in BOUNDS and not valid(p.name, p.value):
                return SetParametersResult(successful=False, reason=f'{p.name}: {BOUNDS[p.name]}')
        return SetParametersResult(successful=True)

    def scan(self, msg):
        self.distance = front_distance(msg.ranges, msg.angle_min, msg.angle_increment)
        self.scan_stamp = time.monotonic()

    def set_mode(self, request, response):
        response.success = request.mode in ('OFF', 'PATROL')
        if response.success:
            self.mode = request.mode
            self.tick()
        response.message = self.mode if response.success else 'Allowed: OFF, PATROL'
        return response

    def tick(self):
        msg = Twist()
        state = 'OFF'
        if self.mode == 'PATROL':
            if self.distance is None or time.monotonic() - self.scan_stamp > 0.5:
                state = 'NO_SCAN'
            elif self.distance < float(self.get_parameter('obstacle_distance').value):
                state = 'TURN'
                msg.angular.z = float(self.get_parameter('turn_speed').value)
            else:
                state = 'ADVANCE'
                msg.linear.x = float(self.get_parameter('speed').value)
        self.publisher.publish(msg)
        status = String()
        status.data = state
        self.state_publisher.publish(status)


def main(args=None):
    rclpy.init(args=args)
    node = Patrol()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
