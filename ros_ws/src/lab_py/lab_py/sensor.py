import math
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from lab_interfaces.msg import Telemetry


class Sensor(Node):
    def __init__(self):
        super().__init__('sensor')
        self.declare_parameter('period', 0.5)
        self.declare_parameter('best_effort', False)
        period = float(self.get_parameter('period').value)
        if not math.isfinite(period) or period <= 0:
            raise ValueError('period must be positive and finite')
        qos = QoSProfile(depth=10, reliability=(
            ReliabilityPolicy.BEST_EFFORT if self.get_parameter('best_effort').value
            else ReliabilityPolicy.RELIABLE))
        self.publisher = self.create_publisher(Telemetry, 'telemetry', qos)
        self.sequence = 0
        self.timer = self.create_timer(period, self.tick)

    def tick(self):
        msg = Telemetry()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        msg.sequence = self.sequence
        msg.voltage = 12.0 + 0.2 * math.sin(self.sequence * 0.2)
        msg.temperature = 35.0 + 3.0 * math.sin(self.sequence * 0.1)
        self.publisher.publish(msg)
        self.sequence = (self.sequence + 1) % (2 ** 32)


def main(args=None):
    rclpy.init(args=args)
    node = Sensor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
