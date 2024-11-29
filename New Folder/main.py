import pyglet
from pyglet import shapes
from pyglet.window import key
import numpy as np
float64 = np.float64

planets = []
circles = []
lines = []
started = False
t = 0
dt = 0.01
G = 30000000

def dist(p1, p2):
    delta_r = p1["pos"] - p2["pos"]
    return np.sqrt(np.inner(delta_r, delta_r))

def fisica():
    global t, planets, circles, G
    t += dt
    for planet in planets:
        planet["acc"] = np.array((0.0, 0.0))
        for body in planets:
            if body["id"] != planet["id"] and dist(planet, body) < 2000:
                delta_r = planet["pos"] - body["pos"]
                planet["acc"] -= G * delta_r / dist(planet, body)**3
        planet["vel"] += planet["acc"] * dt
        planet["pos"] += planet["vel"] * dt

window = pyglet.window.Window()
window.set_size(800, 600)
batch = pyglet.graphics.Batch()
line_batch = pyglet.graphics.Batch()

def stop():
    global t, planets, circles, lines, started, batch, line_batch
    planets = []
    circles = []
    lines = []
    started = False
    t = 0
    batch = pyglet.graphics.Batch()
    line_batch = pyglet.graphics.Batch()

@window.event
def on_mouse_press(x, y, button, modifiers):
    new_circle = shapes.Circle(x, y, 10, batch=batch)
    circles.append(new_circle)

    planets.append({
        "pos": np.array((x, y), dtype=float64),
        "vel": np.array((x, y), dtype=float64),
        "acc": np.array((0.0, 0.0)),
        "id": len(planets)
    })

    new_line = shapes.Line(x, y, x, y, width=5, batch=line_batch)
    lines.append(new_line)

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if len(lines) > 0:
        lines[-1].x2 = x
        lines[-1].y2 = y

@window.event
def on_mouse_release(x, y, button, modifiers):
    planets[-1]["vel"] -= np.array((x, y), dtype=float64)
    planets[-1]["vel"] = -planets[-1]["vel"]

@window.event
def on_key_release(symbol, modifiers):
    global started
    if symbol == key.ENTER:
        started = True

@window.event
def on_draw():
    window.clear()
    batch.draw()
    if started: fisica()
    else: line_batch.draw()
    for i in range(len(circles)):
        circles[i].x = planets[i]["pos"][0]
        circles[i].y = planets[i]["pos"][1]

pyglet.app.run()