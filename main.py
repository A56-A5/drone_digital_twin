import tkinter as tk
from tkinter import scrolledtext
from drone1 import Drone
import pandas as pd

tick_list = list()
battery_list = list()
altitude_list = list()
x_list = list()
y_list = list()
weather_list = list()

MOVE_STEP = 5
ALT_STEP = 5
TICK_MS = 1000  

root = tk.Tk()
root.title("Drone Control")

drone = Drone()
drone.isFlying = True
weather = drone.randomWeather()
tick = 0


def log(msg):
    print(msg)
    log_box.configure(state="normal")
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)
    log_box.configure(state="disabled")


def record_state():
    tick_list.append(tick)
    battery_list.append(drone.battery)
    altitude_list.append(drone.altitude)
    x_list.append(drone.x)
    y_list.append(drone.y)
    weather_list.append(weather['condition'])


def do_tick(climbing=False):
    global tick, weather
    tick += 1

    drained = drone.drainBattery(weather, climbing=climbing)
    dx, dy = drone.applyWind(weather)
    drone.x += dx
    drone.y += dy

    log(f"tick {tick}: now {drone.battery:.1f}%, "
        f"pos ({drone.x:.1f}, {drone.y:.1f}), alt {drone.altitude:.1f}, "
        f"condition {weather['condition']}")

    if tick % 10 == 0:
        weather = drone.randomWeather()
        log(f"weather changed to {weather['condition']}")

    if drone.isLowAltitude():
        log("Low Altitude, please fly higher")
    if drone.isLowBattery():
        log("Low Battery, please recharge")
    if drone.battery <= 0:
        drone.battery = 0
        drone.isFlying = False
        drone.descend()
        log("Battery dead")
    if drone.altitude < 0:
        drone.altitude = 0
        drone.isFlying = False
        log("Drone Crashed")

    record_state()


def move(dx, dy):
    if not drone.isFlying or drone.battery <= 0:
        log("cant move, drone not flying or battery dead")
        return
    drone.x += dx * MOVE_STEP
    drone.y += dy * MOVE_STEP
    log(f"moved to ({drone.x:.1f}, {drone.y:.1f})")
    do_tick(climbing=False)


def climb():
    if not drone.isFlying or drone.battery <= 0:
        log("cant climb, drone not flying or battery dead")
        return
    drone.altitude += ALT_STEP
    log(f"climbing, altitude now {drone.altitude:.1f}")
    do_tick(climbing=True)


def descend():
    if not drone.isFlying or drone.battery <= 0:
        log("cant descend, drone not flying or battery dead")
        return
    drone.altitude = max(0, drone.altitude - ALT_STEP)
    log(f"descending, altitude now {drone.altitude:.1f}")
    do_tick(climbing=False)


def game_loop():
    if drone.isFlying and drone.battery > 0:
        do_tick(climbing=False)
    root.after(TICK_MS, game_loop)


def export_log():
    df = pd.DataFrame({
        "tick": tick_list,
        "battery": battery_list,
        "altitude": altitude_list,
        "x": x_list,
        "y": y_list,
        "weather": weather_list,
    })
    df.to_csv("drone_log.csv", index=False)
    log("exported log to drone_log.csv")
    return df


pad = tk.Frame(root)
pad.grid(row=0, column=0, padx=10, pady=10)

tk.Button(pad, text="W", width=8, command=lambda: move(0, 1)).grid(row=0, column=1)
tk.Button(pad, text="A", width=8, command=lambda: move(-1, 0)).grid(row=1, column=0)
tk.Button(pad, text="D", width=8, command=lambda: move(1, 0)).grid(row=1, column=2)
tk.Button(pad, text="S", width=8, command=lambda: move(0, -1)).grid(row=2, column=1)

tk.Button(pad, text="^", width=8, command=climb).grid(row=3, column=0, pady=(10, 0))
tk.Button(pad, text="v", width=8, command=descend).grid(row=3, column=2, pady=(10, 0))

tk.Button(pad, text="Export CSV", width=18, command=export_log).grid(row=4, column=0, columnspan=3, pady=(10, 0))

log_box = scrolledtext.ScrolledText(root, width=60, height=20, state="disabled")
log_box.grid(row=0, column=1, padx=10, pady=10)

log(f"drone booted up, weather is {weather['condition']}")
record_state()

root.after(TICK_MS, game_loop)
root.mainloop()