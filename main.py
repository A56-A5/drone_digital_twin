import Drone from drone1.py
import math

drone = Drone()

time_stamp = 0
weather = drone.randomWeather()

while drone.isFlying and drone.battery > 0 and drone.altitude > 0:
    time_stamp += 1

    drone.battery -= drone.battery * 0.8
    wind_rad = weather['wind_direction'] * (math.pi / 180)
    wind_dx = weather['wind_speed'] * 0.1 * math.cos(wind_rad)
    wind_dy = weather['wind_speed'] * 0.1 * math.sin(wind_rad)

    drone.x += wind_dx 
    drone.y += wind_dy 

    

    if weather['condition'] == 'rainy':
        drone.battery -= drone.battery * 1.0
    
    if time_stamp % 10 == 0: 
        weather = drone.randomWeather()
        drone.printStatus()

    if drone.isLowAltitude():
        print("Low Altitude !!! \n Please Fly Higher")
    
    if drone.isLowBattery():
        print("Low Battery !!! \n Please Recharge")
        
    if drone.battery <= 0: 
        print("Battery dead")
        break
    
    if drone.altitude < 0:
        print("Drone Crashed")
        break

drone.printStatus()
