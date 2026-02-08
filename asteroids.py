import math
import random
from OpenGL.GL import *

class AsteroidBelt:
    def __init__(self, count=300, inner_radius=10.0, outer_radius=12.0, height=0.5, rotation_speed=5.0):
        """
        count: number of asteroids
        inner_radius, outer_radius: belt radius range
        height: vertical thickness
        rotation_speed: degrees per second for the belt rotation
        """
        self.count = count
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.height = height
        self.rotation_speed = rotation_speed
        self.angle = 0.0  # current rotation angle of the belt
        self.positions = []

        for _ in range(count):
            r = random.uniform(inner_radius, outer_radius)
            theta = random.uniform(0, 360)
            y = random.uniform(-height, height)
            self.positions.append((r, theta, y))

    def draw(self, elapsed_seconds):
        self.angle = (self.angle + self.rotation_speed * elapsed_seconds) % 360.0

        glPushMatrix()
        glRotatef(self.angle, 0, 1, 0)  # rotate entire belt around Y axis

        glDisable(GL_LIGHTING)
        glColor3f(0.6, 0.6, 0.6)
        glBegin(GL_POINTS)
        for r, theta, y in self.positions:
            x = r * math.cos(math.radians(theta))
            z = r * math.sin(math.radians(theta))
            glVertex3f(x, y, z)
        glEnd()
        glEnable(GL_LIGHTING)

        glPopMatrix()
