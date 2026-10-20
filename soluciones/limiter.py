import math


def limit(v, w):
    if not math.isfinite(v) or not math.isfinite(w):
        return 0.0, 0.0
    return max(0.0, min(0.35, v)), max(-1.0, min(1.0, w))
