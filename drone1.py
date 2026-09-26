import random
import math

class Drone:
    def __init__(self, battery=100, x=0, y=0, altitude=0):
        self.battery = battery
        self.isFlying = False
        self.x = x
        self.y = y 
        self.altitude = altitude

    def isLowBattery(self):
        return self.battery <= 20

    def isLowAltitude(self):
        return self.altitude <= 50

    def printStatus():
        print(f'State: {self.isFlying}')
        print(f'Battery = {self.battery}')
        print(f'Position = ({self.x},{self.y})')
        print(f'Altitude = {self.altitude}')
        print(f'')
        print(f'Battery = {"Low" if self.isLowBattery() else "Good"}')
    
    def randomWeather(self):
        wind_speed = random.uniform(0, 20)
        wind_direction = random.uniform(0, 360)
        condition = random.choice(['windy','rainy','normal'])

        return {'wind_speed': wind_speed, 'wind_direction': wind_direction, 'condition': condition}

