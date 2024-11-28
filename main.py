import pyglet
from pyglet import shapes
import numpy as np
float64 = np.float64

planets = []
circles = []
t = 0
dt = 0.01

def dist(p1, p2):
    delta_r = p1["pos"] - p2["pos"]
    return np.sqrt(np.inner(delta_r, delta_r))

def fisica():
    global t, planets, circles
    t += dt
    for planet in planets:
        planet["acc"] = np.array((0.0, 0.0))
        for bodie in planets:
            if bodie != planet:
                delta_r = planet["pos"] - bodie["pos"]
                planet["acc"] += delta_r / dist(planet, bodie)**3
        planet["vel"] += planet["acc"] * dt
        planet["pos"] += planet["vel"] * dt

window = pyglet.window.Window()
window.set_size(800, 600)
batch = pyglet.graphics.Batch()

@window.event
def on_mouse_press(x, y, button, modifiers):
    new_circle = shapes.Circle(x, y, 25, batch=batch)
    circles.append(new_circle)

    planets.append({
        "pos": np.array((x, y), dtype=float64),
        "vel": np.array((x, y), dtype=float64),
        "acc": np.array((0.0, 0.0))
    })

@window.event
def on_mouse_release(x, y, button, modifiers):
    planets[-1]["vel"] -= np.array((x, y), dtype=float64)
    print(planets)

@window.event
def on_draw():
    fisica()
    for i in range(len(circles)):
        circles[i].x = planets[i]["pos"][0]
        circles[i].y = planets[i]["pos"][1]
    window.clear()
    batch.draw()



pyglet.app.run()