import tkinter as tk
from tkinter import scrolledtext
from drone1 import Drone

MOVE_STEP = 5
ALT_STEP = 5

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

def do_tick(climbing=False):
    global tick, weather
    tick += 1
    drained = drone.drainBattery(weather, climbing=climbing)
    dx, dy = drone.applyWind(weather)

    log(f"battery -{drained:.2f}%, now {drone.battery:.1f}%, condition {weather['condition']}")

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
        log("Battery dead")
    if drone.altitude < 0:
        drone.altitude = 0
        drone.isFlying = False
        log("Drone Crashed")

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


pad = tk.Frame(root)
pad.grid(row=0, column=0, padx=10, pady=10)

tk.Button(pad, text="W", width=8, command=lambda: move(0, 1)).grid(row=0, column=1)
tk.Button(pad, text="A", width=8, command=lambda: move(-1, 0)).grid(row=1, column=0)
tk.Button(pad, text="D", width=8, command=lambda: move(1, 0)).grid(row=1, column=2)
tk.Button(pad, text="S", width=8, command=lambda: move(0, -1)).grid(row=2, column=1)

tk.Button(pad, text="U", width=8, command=climb).grid(row=3, column=0, pady=(10, 0))
tk.Button(pad, text="D", width=8, command=descend).grid(row=3, column=2, pady=(10, 0))

log_box = scrolledtext.ScrolledText(root, width=50, height=20, state="disabled")
log_box.grid(row=0, column=1, padx=10, pady=10)

log(f"drone booted up, weather is {weather['condition']}")

root.mainloop()