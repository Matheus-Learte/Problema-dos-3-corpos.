from threading import Thread
import pyglet
from pyglet import shapes
from pyglet.window import key
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import sys
float64 = np.float64

planets = []
lines = []
started = False
t = 0
dt = 0.01
G = 3000

### MATPLOTLIB
N = 400
fig, axs = plt.subplots(2,1, figsize=(6, 8))
X = np.linspace(t - N * dt, t, N)
Y1 = np.zeros(N)
Y2 = np.zeros(N)
Y3 = np.zeros(N)
Y4 = np.zeros(N)
Y5 = np.zeros(N)
Y6 = np.zeros(N)
plot1 = axs[0].plot(X, Y1, label="Aceleração, eixo X")[0]
plot2 = axs[0].plot(X, Y2, label="Aceleração, eixo Y")[0]
plot3 = axs[0].plot(X, Y3, label="Aceleração, modulo")[0]
plot4 = axs[1].plot(X, Y4, label="Velocidade, eixo X")[0]
plot5 = axs[1].plot(X, Y5, label="Velocidade, eixo Y")[0]
plot6 = axs[1].plot(X, Y6, label="Velocidade, modulo")[0]
axs[0].legend()
axs[1].legend()

fig.canvas.draw()
background = fig.canvas.copy_from_bbox(fig.bbox)

def update_plot():
    global t, X, Y1, Y2, Y3, Y4, Y5, Y6
    body = planets[-1]
    X = X + dt

    Y1 = np.roll(Y1, -1)
    Y2 = np.roll(Y2, -1)
    Y3 = np.roll(Y3, -1)
    Y4 = np.roll(Y4, -1)
    Y5 = np.roll(Y5, -1)
    Y6 = np.roll(Y6, -1)

    Y1[-1] = body["acc"][0]
    Y2[-1] = body["acc"][1]
    Y3[-1] = np.linalg.norm(body["acc"])
    Y4[-1] = body["vel"][0]
    Y5[-1] = body["vel"][1]
    Y6[-1] = np.linalg.norm(body["vel"])

    plot1.set_data(X, Y1)
    plot2.set_data(X, Y2)
    plot3.set_data(X, Y3)
    plot4.set_data(X, Y4)
    plot5.set_data(X, Y5)
    plot6.set_data(X, Y6)

    axs[0].set_xlim(min(X), max(X))
    axs[1].set_xlim(min(X), max(X))
    mi1 = min(min(Y1), min(Y2), min(Y3))
    mi2 = min(min(Y4), min(Y5), min(Y6))
    ma1 = max(max(Y1), max(Y2), max(Y3))
    ma2 = max(max(Y4), max(Y5), max(Y6))
    mi1 -= 0.2*abs(ma1-mi1)
    mi2 -= 0.2*abs(ma2-mi2)
    ma1 += 0.2*abs(ma1-mi1)
    ma2 += 0.2*abs(ma2-mi2)
    axs[0].set_ylim(mi1, ma1)
    axs[1].set_ylim(mi2, ma2)

    fig.canvas.restore_region(background)
    axs[0].draw_artist(plot1)
    axs[0].draw_artist(plot2)
    axs[0].draw_artist(plot3)
    axs[1].draw_artist(plot4)
    axs[1].draw_artist(plot5)
    axs[1].draw_artist(plot6)

    fig.canvas.blit(fig.bbox)
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

def stop():
    global t, planets, lines, started, batch, line_batch
    planets = []
    lines = []
    started = False
    t = 0
    line_batch = pyglet.graphics.Batch()

@window.event
def on_mouse_press(x, y, button, modifiers):
    global started
    if started: return
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
    global started
    if started: return
    if len(lines) > 0:
        lines[-1].x2 = x
        lines[-1].y2 = y

@window.event
def on_mouse_release(x, y, button, modifiers):
    global started
    if started: return
    planets[-1]["vel"] -= np.array((x, y), dtype=float64)
    planets[-1]["vel"] = -1*planets[-1]["vel"]

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
            planets[-1]["mass"] = 10
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

# sistema circular sol-terra
def preset1():
    global planets
    planets.append({
        "pos": np.array((400.0, 300.0)),
        "vel": np.array((0.0, 0.0)),
        "acc": np.array((0.0, 0.0)),
        "mass": 10000,
        "img": sol,
        "id": len(planets)
    })
    planets.append({
        "pos": np.array((600.0, 300.0)),
        "vel": np.array((0.0, -389.0)),
        "acc": np.array((0.0, 0.0)),
        "mass": 100,
        "img": terra,
        "id": len(planets)
    })

# sistema circular terra-lua
def preset2():
    global planets
    planets.append({
        "pos": np.array((400.0, 300.0)),
        "vel": np.array((0.0, 0.0)),
        "acc": np.array((0.0, 0.0)),
        "mass": 100,
        "img": terra,
        "id": len(planets)
    })
    planets.append({
        "pos": np.array((450.0, 300.0)),
        "vel": np.array((0.0, -78.0)),
        "acc": np.array((0.0, 0.0)),
        "mass": 1,
        "img": lua,
        "id": len(planets)
    })

# sistema elíptico sol-terra
def preset3():
    global planets
    planets.append({
        "pos": np.array((400.0, 300.0)),
        "vel": np.array((0.0, 0.0)),
        "acc": np.array((0.0, 0.0)),
        "mass": 10000,
        "img": sol,
        "id": len(planets)
    })
    planets.append({
         "pos": np.array((600.0, 300.0)),
         "vel": np.array((0.0, -200.0)),
         "acc": np.array((0.0, 0.0)),
         "mass": 100,
        "img": terra,
        "id": len(planets)
    })

# dois sóis se colidindo
def preset4():
    global planets
    planets.append({
        "pos": np.array((100.0, 300.0)),
        "vel": np.array((0.0, 0.0)),
        "acc": np.array((0.0, 0.0)),
        "mass": 10000,
        "img": sol,
        "id": len(planets)
    })
    planets.append({
        "pos": np.array((700.0, 300.0)),
        "vel": np.array((0.0, 0.0)),
        "acc": np.array((0.0, 0.0)),
        "mass": 10000,
        "img": sol,
        "id": len(planets)
    })

# sistema de três corpos caótico
def preset5():
    global planets
    planets.append({
        "pos": np.array((200.0, 500.0)),
        "vel": np.array((0.0, 0.0)),
        "acc": np.array((0.0, 0.0)),
        "mass": 10000,
        "img": sol,
        "id": len(planets)
    })
    planets.append({
        "pos": np.array((600.0, 500.0)),
        "vel": np.array((0.0, 0.0)),
        "acc": np.array((0.0, 0.0)),
        "mass": 10000,
        "img": sol,
        "id": len(planets)
    })
    planets.append({
        "pos": np.array((400.0, 153.0)),
        "vel": np.array((-300.0, 300.0)),
        "acc": np.array((0.0, 0.0)),
        "mass": 10000,
        "img": sol,
        "id": len(planets)
    })
    planets[0]["vel"] = (planets[1]["pos"] - planets[0]["pos"]) * 0.7
    planets[1]["vel"] = (planets[2]["pos"] - planets[1]["pos"]) * 0.7

if __name__ == "__main__":
    if len(sys.argv) > 1:
        a = sys.argv[1]
    else:
        a = 0
    if a == "1":
        preset1()
    elif a == "2":
        preset2()
    elif a == "3":
        preset3()
    elif a == "4":
        preset4()
    elif a == "5":
        preset5()

    pyglet.app.run()