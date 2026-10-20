"""Small deterministic functions, deliberately independent of ROS."""
import math


def integrate(x, y, yaw, speed, turn, dt):
    """Exact constant-twist unicycle integration (SI units)."""
    if not all(math.isfinite(v) for v in (x, y, yaw, speed, turn, dt)) or dt < 0:
        raise ValueError('Non-finite state or negative dt')
    if abs(turn) < 1e-9:
        x += speed * math.cos(yaw) * dt
        y += speed * math.sin(yaw) * dt
    else:
        x += speed / turn * (math.sin(yaw + turn * dt) - math.sin(yaw))
        y -= speed / turn * (math.cos(yaw + turn * dt) - math.cos(yaw))
    yaw = math.atan2(math.sin(yaw + turn * dt), math.cos(yaw + turn * dt))
    return x, y, yaw


def ray_circle(x, y, angle, circle, max_range=6.0):
    """Nearest positive intersection of a ray with a circle, or max_range."""
    cx, cy, radius = circle
    dx, dy = cx - x, cy - y
    if dx * dx + dy * dy <= radius * radius:
        return 0.0
    projection = dx * math.cos(angle) + dy * math.sin(angle)
    discriminant = radius * radius - (dx * dx + dy * dy - projection ** 2)
    if discriminant < 0:
        return max_range
    distance = projection - math.sqrt(max(0.0, discriminant))
    return min(max_range, distance) if distance >= 0 else max_range


def front_distance(ranges, angle_min, angle_increment, half_angle=0.5):
    """+inf means clear; NaN, negative and -inf are invalid data."""
    values = [r for i, r in enumerate(ranges)
              if abs(angle_min + i * angle_increment) <= half_angle
              and not math.isnan(r) and r >= 0]
    return min(values) if values else None


def guarded_command(v, w, command_age, scan_age, distance, emergency=False):
    """Didactic gate: stale/invalid data stops, front obstacle blocks forward."""
    if emergency or not all(math.isfinite(a) for a in (v, w, command_age, scan_age)):
        return 0.0, 0.0
    if not (0 <= command_age <= 0.5 and 0 <= scan_age <= 0.5):
        return 0.0, 0.0
    if distance is None or math.isnan(distance) or distance < 0:
        return 0.0, 0.0
    # No rear sensor: this exercise does not permit reversing.
    v = min(0.35, max(0.0, v))
    w = min(1.0, max(-1.0, w))
    if distance < 0.55:
        v = 0.0
    return v, w
