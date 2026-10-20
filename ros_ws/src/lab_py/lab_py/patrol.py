import math
import time
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from rcl_interfaces.msg import SetParametersResult
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from lab_interfaces.srv import SetMode
from .core import front_distance


class Patrol(Node):
    def __init__(self):
        super().__init__('patrol')
        self.declare_parameter('speed', 0.2)
        self.declare_parameter('turn_speed', 0.65)
        self.add_on_set_parameters_callback(self.validate_parameters)
        for name, maximum in [('speed', 0.35), ('turn_speed', 1.0)]:
            value = float(self.get_parameter(name).value)
            if not math.isfinite(value) or not 0 <= value <= maximum:
                raise ValueError(f'{name} outside allowed range')
        self.mode = 'OFF'
        self.distance = None
        self.scan_stamp = 0.0
        self.publisher = self.create_publisher(Twist, 'cmd_vel_raw', 10)
        self.scan_sub = self.create_subscription(LaserScan, 'scan', self.scan, qos_profile_sensor_data)
        self.mode_srv = self.create_service(SetMode, 'set_mode', self.set_mode)
        self.timer = self.create_timer(0.1, self.tick)

    def validate_parameters(self, params):
        for p in params:
            maximum = {'speed': 0.35, 'turn_speed': 1.0}.get(p.name)
            if maximum is not None:
                if type(p.value) not in (float, int) or not math.isfinite(p.value) or not 0 <= p.value <= maximum:
                    return SetParametersResult(successful=False, reason=f'{p.name}: allowed 0..{maximum}')
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
        if self.mode == 'PATROL' and self.distance is not None and time.monotonic() - self.scan_stamp <= 0.5:
            if self.distance < 0.85:
                msg.angular.z = float(self.get_parameter('turn_speed').value)
            else:
                msg.linear.x = float(self.get_parameter('speed').value)
        self.publisher.publish(msg)


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
