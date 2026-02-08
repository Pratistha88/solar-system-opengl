import math
from utils import clamp, deg2rad

class Camera:
    def __init__(self):
        self.distance = 45.0
        self.yaw_deg = 0.0
        self.pitch_deg = 18.0
        self.target = (0.0, 0.0, 0.0)

    def apply_gluLookAt(self, gluLookAt):
        yaw = deg2rad(self.yaw_deg)
        pitch = deg2rad(self.pitch_deg)

        cx = self.distance * math.cos(pitch) * math.sin(yaw)
        cy = self.distance * math.sin(pitch)
        cz = self.distance * math.cos(pitch) * math.cos(yaw)

        tx, ty, tz = self.target
        gluLookAt(cx+tx, cy+ty, cz+tz,
                  tx, ty, tz,
                  0.0, 1.0, 0.0)

    def zoom(self, delta):
        self.distance = clamp(self.distance + delta, 6.0, 120.0)

    def rotate(self, yaw_delta=0.0, pitch_delta=0.0):
        self.yaw_deg = (self.yaw_deg + yaw_delta) % 360.0
        self.pitch_deg = clamp(self.pitch_deg + pitch_delta, -80.0, 80.0)
