#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from lab_interfaces.msg import Telemetry


class BatteryAlarm(Node):
    def __init__(self):
        super().__init__('battery_alarm')
        self.publisher = self.create_publisher(String, 'battery_alarm', 10)
        self.subscription = self.create_subscription(Telemetry, 'telemetry', self.receive, 10)

    def receive(self, msg):
        if msg.voltage < 11.9:
            alarm = String()
            alarm.data = f'LOW_VOLTAGE sequence={msg.sequence} voltage={msg.voltage:.3f} V'
            self.publisher.publish(alarm)


def main():
    rclpy.init()
    node = BatteryAlarm()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
