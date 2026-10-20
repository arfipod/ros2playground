import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'ros_ws/src/lab_py'))
from lab_py.core import integrate, ray_circle, front_distance, guarded_command


class KinematicsTest(unittest.TestCase):
    def test_straight(self):
        self.assertEqual(integrate(0, 0, 0, 1, 0, 2), (2, 0, 0))

    def test_quarter_circle(self):
        x, y, yaw = integrate(0, 0, 0, 1, 1, math.pi / 2)
        for actual, expected in zip((x, y, yaw), (1, 1, math.pi / 2)):
            self.assertAlmostEqual(actual, expected)

    def test_rotation_in_place(self):
        x, y, _ = integrate(2, 3, 0, 0, 1, 2)
        self.assertEqual((x, y), (2, 3))

    def test_invalid_input(self):
        for dt in [-1, math.nan, math.inf]:
            with self.assertRaises(ValueError):
                integrate(0, 0, 0, 1, 0, dt)


class LidarTest(unittest.TestCase):
    def test_hit(self):
        self.assertAlmostEqual(ray_circle(0, 0, 0, (2, 0, 0.5)), 1.5)

    def test_miss_and_behind(self):
        self.assertEqual(ray_circle(0, 0, math.pi / 2, (2, 0, 0.5)), 6.0)
        self.assertEqual(ray_circle(0, 0, math.pi, (2, 0, 0.5)), 6.0)

    def test_inside(self):
        self.assertEqual(ray_circle(2, 0, 0, (2, 0, 0.5)), 0.0)

    def test_sector(self):
        self.assertEqual(front_distance([0.1, 3, 0.2], -1, 1), 3)

    def test_invalid_and_infinite(self):
        self.assertIsNone(front_distance([math.nan, -1, -math.inf], -0.1, 0.1))
        self.assertEqual(front_distance([math.inf], 0, 0.1), math.inf)
        self.assertIsNone(front_distance([], 0, 0.1))


class GateTest(unittest.TestCase):
    def gate(self, **overrides):
        values = dict(v=0.2, w=0.1, command_age=0.1, scan_age=0.1, distance=2.0)
        values.update(overrides)
        return guarded_command(**values)

    def test_valid(self):
        self.assertEqual(self.gate(), (0.2, 0.1))

    def test_stale(self):
        self.assertEqual(self.gate(command_age=0.51), (0, 0))
        self.assertEqual(self.gate(scan_age=0.51), (0, 0))

    def test_latched(self):
        self.assertEqual(self.gate(emergency=True), (0, 0))

    def test_limit(self):
        self.assertEqual(self.gate(v=5, w=-5), (0.35, -1.0))

    def test_reverse_blocked(self):
        self.assertEqual(self.gate(v=-1), (0, 0.1))

    def test_obstacle(self):
        self.assertEqual(self.gate(distance=0.4), (0, 0.1))

    def test_missing_sensor(self):
        self.assertEqual(self.gate(distance=None), (0, 0))

    def test_nonfinite(self):
        for invalid in (math.nan, math.inf, -math.inf):
            self.assertEqual(self.gate(v=invalid), (0, 0))
        self.assertEqual(self.gate(distance=math.nan), (0, 0))
        self.assertEqual(self.gate(distance=math.inf), (0.2, 0.1))


if __name__ == '__main__':
    unittest.main()
