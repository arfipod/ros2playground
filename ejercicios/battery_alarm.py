#!/usr/bin/env python3
"""Práctica 02: completa SOLO el callback receive."""
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
        # TODO: si voltage < 11.9, publica secuencia y voltaje como String.
        raise NotImplementedError('Completa el ejercicio antes de ejecutar')


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
