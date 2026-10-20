#!/usr/bin/env python3
import math
import unittest
from limiter import limit


class LimiterTest(unittest.TestCase):
    def test_inside(self):
        self.assertEqual(limit(0.2, 0.5), (0.2, 0.5))

    def test_clamp(self):
        self.assertEqual(limit(2, -5), (0.35, -1))
        self.assertEqual(limit(-2, 5), (0, 1))

    def test_nonfinite(self):
        for invalid in (math.nan, math.inf, -math.inf):
            self.assertEqual(limit(invalid, 0), (0, 0))
            self.assertEqual(limit(0, invalid), (0, 0))


if __name__ == '__main__':
    unittest.main()
