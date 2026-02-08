import os
import math
import random

def clamp(x, lo, hi):
    return max(lo, min(hi, x))

def deg2rad(deg: float) -> float:
    return deg * math.pi / 180.0

def ensure_path(path: str) -> str:
    return os.path.abspath(path)

def try_import_pil():
    try:
        from PIL import Image  # type: ignore
        return Image
    except Exception:
        return None

def generate_stars(count=800, radius=120):
    stars = []
    for _ in range(count):
        x = random.uniform(-radius, radius)
        y = random.uniform(-radius, radius)
        z = random.uniform(-radius, radius)
        brightness = random.uniform(0.5, 1.0)
        stars.append((x, y, z, brightness))
    return stars
