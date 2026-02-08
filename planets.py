from dataclasses import dataclass
from typing import Optional, Tuple, List

from OpenGL.GL import *
from OpenGL.GLU import *


@dataclass
class Planet:
    name: str
    orbit_radius: float
    radius: float
    color: Tuple[float, float, float]
    revolution_speed: float
    rotation_speed: float
    texture_path: Optional[str] = None
    texture_id: Optional[int] = None
    tilt_angle: float = 0.0

    revolution_angle: float = 0.0
    rotation_angle: float = 0.0


class SolarSystem:
    def __init__(self, planets: List[Planet], sun_texture_path: Optional[str] = None):
        self.planets = planets
        self.sun_texture_path = sun_texture_path
        self.sun_texture_id: Optional[int] = None

        self.time_scale = 1.0
        self.paused = False
        self.show_orbits = True
        self.use_textures = True

    # Controls
    def toggle_pause(self):
        self.paused = not self.paused

    def toggle_orbits(self):
        self.show_orbits = not self.show_orbits

    def toggle_textures(self):
        self.use_textures = not self.use_textures

    def set_time_scale(self, scale):
        self.time_scale = max(0.05, min(10.0, scale))

    # Texture loading
    def load_textures(self, load_texture_func):
        if self.sun_texture_path:
            self.sun_texture_id = load_texture_func(self.sun_texture_path)
        for p in self.planets:
            if p.texture_path:
                p.texture_id = load_texture_func(p.texture_path)

    # Drawing helpers
    def _draw_orbit(self, radius: float):
        glDisable(GL_LIGHTING)
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_LINE_LOOP)
        for i in range(180):
            theta = (2.0 * 3.14159265 * i) / 180.0
            x = radius * __import__("math").cos(theta)
            z = radius * __import__("math").sin(theta)
            glVertex3f(x, 0.0, z)
        glEnd()
        glEnable(GL_LIGHTING)

    def _draw_saturn_rings(self, inner_radius, outer_radius):
        glDisable(GL_LIGHTING)
        glColor3f(0.8, 0.75, 0.6)
        glBegin(GL_QUAD_STRIP)
        for i in range(0, 361, 5):
            angle = i * 3.14159265 / 180.0
            x_inner = inner_radius * __import__("math").cos(angle)
            z_inner = inner_radius * __import__("math").sin(angle)
            x_outer = outer_radius * __import__("math").cos(angle)
            z_outer = outer_radius * __import__("math").sin(angle)
            glVertex3f(x_inner, 0.0, z_inner)
            glVertex3f(x_outer, 0.0, z_outer)
        glEnd()
        glEnable(GL_LIGHTING)

    def _draw_textured_sphere(self, quad, radius: float, texture_id: Optional[int]):
        if texture_id is not None:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            gluQuadricTexture(quad, GL_TRUE)
        else:
            glDisable(GL_TEXTURE_2D)
            gluQuadricTexture(quad, GL_FALSE)
        gluSphere(quad, radius, 48, 48)
        if texture_id is not None:
            glBindTexture(GL_TEXTURE_2D, 0)
            glDisable(GL_TEXTURE_2D)

    # Main draw
    def draw(self, elapsed_seconds: float):
        if self.paused:
            elapsed_seconds = 0.0

        quad = gluNewQuadric()
        gluQuadricNormals(quad, GLU_SMOOTH)

        # Sun
        glPushMatrix()
        tex = self.sun_texture_id if (self.use_textures and self.sun_texture_id) else None
        self._draw_textured_sphere(quad, 2.2, tex)
        glPopMatrix()

        # Planets
        for p in self.planets:
            if self.show_orbits:
                self._draw_orbit(p.orbit_radius)

            glPushMatrix()

            # Revolution
            p.revolution_angle = (p.revolution_angle + p.revolution_speed * elapsed_seconds) % 360.0
            glRotatef(p.revolution_angle, 0.0, 1.0, 0.0)
            glTranslatef(p.orbit_radius, 0.0, 0.0)

            # Tilt
            glRotatef(p.tilt_angle, 0.0, 0.0, 1.0)

            # Self rotation
            p.rotation_angle = (p.rotation_angle + p.rotation_speed * elapsed_seconds) % 360.0
            glRotatef(p.rotation_angle, 0.0, 1.0, 0.0)

            # Planet body
            tex = p.texture_id if (self.use_textures and p.texture_id) else None
            self._draw_textured_sphere(quad, p.radius, tex)

            # Saturn rings
            if p.name.lower() == "saturn":
                glPushMatrix()
                glRotatef(90, 1, 0, 0)
                self._draw_saturn_rings(p.radius*1.4, p.radius*2.2)
                glPopMatrix()

            glPopMatrix()

        gluDeleteQuadric(quad)
