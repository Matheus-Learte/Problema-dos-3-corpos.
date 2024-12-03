from threading import Thread
import pyglet
from pyglet import shapes
from pyglet.window import key
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
float64 = np.float64

bg = pyglet.image.load('img/bg.png')
terra = pyglet.image.load('img/terra_50.png')
sol = pyglet.image.load('img/sol_70.png')
lua = pyglet.image.load('img/lua_10.png')
terra.anchor_x = terra.width // 2
terra.anchor_y = terra.height // 2
sol.anchor_x = sol.width // 2
sol.anchor_y = sol.height // 2
lua.anchor_x = lua.width // 2
lua.anchor_y = lua.height // 2

planets = []
lines = []
started = False
t = 0
dt = 0.01
G = 3000

### MATPLOTLIB
fig, ax = plt.subplots()
X = []
Y1 = []
Y2 = []
Y_res = []
plot1 = ax.plot(X, Y1, label="Velocidade, eixo X")[0]
plot2 = ax.plot(X, Y2, label="Velocidade, eixo Y")[0]
plot3 = ax.plot(X, Y_res, label="Velocidade Resultante")[0]
ax.legend()

N = 400
def update_plot():
    global t

    earth = {}
    for planet in planets:
        if planet["mass"] == 100: earth = planet

    X = np.linspace(t-N*dt, t, N)

    Y1.append(earth["vel"][0])
    if len(Y1) > N: Y1.pop(0)
    Y2.append(earth["vel"][1])
    if len(Y2) > N: Y2.pop(0)

    v_res = np.sqrt(earth["vel"][0]**2 + earth["vel"][1]**2)
    Y_res.append(v_res)
    if len(Y_res) > N: Y_res.pop(0)

    plot1.set_xdata(X[-len(Y1):])
    plot2.set_xdata(X[-len(Y2):])
    plot1.set_ydata(Y1)
    plot2.set_ydata(Y2)
    plot3.set_xdata(X[-len(Y_res):])
    plot3.set_ydata(Y_res)

    ax.set_xlim(min(X), max(X))
    ax.set_ylim(min(min(Y1), min(Y2), min(Y_res)), 
            max(max(Y1), max(Y2), max(Y_res)))
    fig.canvas.draw()
    fig.canvas.flush_events()

### FÍSICA

def dist(p1, p2):
    delta_r = p1["pos"] - p2["pos"]
    return np.sqrt(np.inner(delta_r, delta_r))

def fisica():
    global t, planets, G
    t += dt
    for planet in planets:
        planet["acc"] = np.array((0.0, 0.0))
        for body in planets:
            if body["id"] != planet["id"] and dist(planet, body) < 2000:
                delta_r = planet["pos"] - body["pos"]
                M = body["mass"]
                m = planet["mass"]
                planet["acc"] -= G * M * delta_r / dist(planet, body)**3
        planet["vel"] += planet["acc"] * dt
        planet["pos"] += planet["vel"] * dt

### PYGLET

window = pyglet.window.Window()
window.set_size(800, 600)
line_batch = pyglet.graphics.Batch()

def stop():
    global t, planets, lines, started, batch, line_batch
    planets = []
    lines = []
    started = False
    t = 0
    line_batch = pyglet.graphics.Batch()

@window.event
def on_mouse_press(x, y, button, modifiers):
    planets.append({
        "pos": np.array((x, y), dtype=float64),
        "vel": np.array((x, y), dtype=float64),
        "acc": np.array((0.0, 0.0)),
        "mass": 100,
        "img": terra,
        "id": len(planets)
    })

    new_line = shapes.Line(x, y, x, y, width=2, batch=line_batch)
    lines.append(new_line)

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if len(lines) > 0:
        lines[-1].x2 = x
        lines[-1].y2 = y

@window.event
def on_mouse_release(x, y, button, modifiers):
    planets[-1]["vel"] -= np.array((x, y), dtype=float64)
    planets[-1]["vel"] = -2 *planets[-1]["vel"]

@window.event
def on_key_release(symbol, modifiers):
    global started
    if symbol == key.ENTER:
        started = True
        plt.ion()
        plt.show(block=False)
    if symbol == key.R:
        stop()
    if len(planets) > 0:
        if symbol == key._1:
            planets[-1]["img"] = lua
            planets[-1]["mass"] = 1
        if symbol == key._2:
            planets[-1]["img"] = terra
            planets[-1]["mass"] = 100
        if symbol == key._3:
            planets[-1]["img"] = sol
            planets[-1]["mass"] = 10000

@window.event
def on_draw():
    window.clear()
    bg.blit(0,0)
    if started:
        fisica()
        update_plot()
    else: line_batch.draw()
    for i in range(len(planets)):
        x = planets[i]["pos"][0]
        y = planets[i]["pos"][1]
        planets[i]["img"].blit(x, y)

pyglet.app.run()
