import sys
import time
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from camera import Camera
from planets import Planet, SolarSystem
from utils import ensure_path, try_import_pil, generate_stars

# -----------------------------
# Global app state
# -----------------------------
W, H = 1000, 700
last_time = time.time()
stars = generate_stars()
camera = Camera()

# Create planets
solar = SolarSystem(
    planets=[
        Planet("Mercury", orbit_radius=4.0,  radius=0.35, color=(0.7, 0.7, 0.7),
               revolution_speed=5.0, rotation_speed=10.0, texture_path="textures/mercury.jpg"),

        Planet("Venus", orbit_radius=5.5,  radius=0.55, color=(0.9, 0.8, 0.5),
               revolution_speed=4.0, rotation_speed=8.0, texture_path="textures/venus.jpg"),

        Planet("Earth", orbit_radius=7.5,  radius=0.60, color=(0.2, 0.4, 1.0),
               revolution_speed=3.0, rotation_speed=12.0, texture_path="textures/earth.jpg"),

        Planet("Mars", orbit_radius=9.5,  radius=0.45, color=(0.9, 0.3, 0.2),
               revolution_speed=2.5, rotation_speed=10.0, texture_path="textures/mars.jpg"),

        Planet("Jupiter", orbit_radius=12.5, radius=1.25, color=(0.9, 0.7, 0.5),
               revolution_speed=1.5, rotation_speed=15.0, texture_path="textures/jupiter.jpg"),

        Planet("Saturn", orbit_radius=16.0, radius=1.10, color=(0.9, 0.85, 0.6),
               revolution_speed=1.2, rotation_speed=14.0, texture_path="textures/saturn.jpg"),

        Planet("Uranus", orbit_radius=19.5, radius=0.90, color=(0.6, 0.8, 0.9),
               revolution_speed=0.8, rotation_speed=12.0, texture_path="textures/uranus.jpg"),

        Planet("Neptune", orbit_radius=23.0, radius=0.85, color=(0.3, 0.4, 0.9),
               revolution_speed=0.6, rotation_speed=11.0, texture_path="textures/neptune.jpg"),
    ],
    sun_texture_path="textures/sun.jpg"
)

# Optional: slow motion for realism
solar.set_time_scale(0.2)

# -----------------------------
# Star background
# -----------------------------
def draw_stars():
    glDisable(GL_LIGHTING)
    glPointSize(1.5)
    glBegin(GL_POINTS)
    glColor3f(1.0, 1.0, 1.0)
    for x, y, z in stars:
        glVertex3f(x, y, z)
    glEnd()
    glEnable(GL_LIGHTING)

# -----------------------------
# Texture loader
# -----------------------------
def load_texture(path: str):
    Image = try_import_pil()
    full = ensure_path(path)

    if Image is None:
        return None

    try:
        img = Image.open(full).convert("RGBA")
    except Exception:
        return None

    img_data = img.tobytes("raw", "RGBA", 0, -1)
    width, height = img.size

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    glBindTexture(GL_TEXTURE_2D, 0)
    return tex_id

# -----------------------------
# OpenGL setup
# -----------------------------
def init_gl():
    global solar   # 🔥 IMPORTANT FIX

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glLightfv(GL_LIGHT0, GL_POSITION, [0, 0, 0, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  [1, 1, 1, 1])
    glLightfv(GL_LIGHT0, GL_AMBIENT,  [0.15, 0.15, 0.15, 1])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 1, 1, 1])

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    glMaterialfv(GL_FRONT, GL_SPECULAR, [1, 1, 1, 1])
    glMaterialf(GL_FRONT, GL_SHININESS, 50)

    solar.load_textures(load_texture)

# -----------------------------
# Drawing
# -----------------------------
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    camera.apply_gluLookAt(gluLookAt)

    global last_time
    now = time.time()
    dt = now - last_time
    last_time = now

    if solar.paused:
        dt = 0.0

    dt *= solar.time_scale

    draw_stars()
    solar.draw(dt * 60.0)

    glutSwapBuffers()

def reshape(w, h):
    if h == 0:
        h = 1
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, w / h, 0.5, 300)
    glMatrixMode(GL_MODELVIEW)

def idle():
    glutPostRedisplay()

# -----------------------------
# Input
# -----------------------------
def keyboard(key, x, y):
    key = key.decode().lower()

    if key == 'q' or ord(key) == 27:
        sys.exit(0)
    elif key == 'w':
        camera.zoom(-1.5)
    elif key == 's':
        camera.zoom(1.5)
    elif key == '+':
        solar.set_time_scale(solar.time_scale + 0.1)
    elif key == '-':
        solar.set_time_scale(solar.time_scale - 0.1)
    elif key == 'p':
        solar.toggle_pause()
    elif key == 'o':
        solar.toggle_orbits()
    elif key == 't':
        solar.toggle_textures()

def special_keys(key, x, y):
    if key == GLUT_KEY_LEFT:
        camera.rotate(yaw_delta=-3)
    elif key == GLUT_KEY_RIGHT:
        camera.rotate(yaw_delta=3)
    elif key == GLUT_KEY_UP:
        camera.rotate(pitch_delta=2)
    elif key == GLUT_KEY_DOWN:
        camera.rotate(pitch_delta=-2)

# -----------------------------
# Main
# -----------------------------
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(W, H)
    glutCreateWindow(b"Solar System - Python OpenGL")

    init_gl()

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutIdleFunc(idle)

    glutMainLoop()

if __name__ == "__main__":
    main()
