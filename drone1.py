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

    def printStatus(self):
        lines = []
        lines.append(f'State: {"Flying" if self.isFlying else "Grounded"}')
        lines.append(f'Battery = {self.battery:.1f}%')
        lines.append(f'Position = ({self.x:.1f}, {self.y:.1f})')
        lines.append(f'Altitude = {self.altitude:.1f}')
        lines.append(f'Battery status = {"Low" if self.isLowBattery() else "Good"}')
        text = "\n".join(lines)
        print(text)
        return text

    def randomWeather(self):
        wind_speed = random.uniform(0, 20)
        wind_direction = random.uniform(0, 360)
        condition = random.choice(['windy', 'rainy', 'normal'])
        return {
            'wind_speed': wind_speed,
            'wind_direction': wind_direction,
            'condition': condition,
        }

    def drainBattery(self, weather, climbing=False):
        drain = self.battery * 0.008

        if weather['condition'] == 'rainy':
            drain += self.battery * 0.01

        if climbing and self.altitude > 50:
            drain += self.battery * 0.005

        self.battery = max(0, self.battery - drain)
        return drain

    def applyWind(self, weather):
        wind_rad = weather['wind_direction'] * (math.pi / 180)
        wind_dx = weather['wind_speed'] * 0.1 * math.cos(wind_rad)
        wind_dy = weather['wind_speed'] * 0.1 * math.sin(wind_rad)
        self.x += wind_dx
        self.y += wind_dy
        return wind_dx, wind_dy