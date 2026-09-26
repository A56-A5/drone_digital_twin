class Drone:
    def __init__(self, battery=100, x=0, y=0, altitude=0):
        self.battery = battery
        self.isFlying = False
        self.x = x
        self.y = y 
        self.altitude = altitude

    def printStatus():

        print(f'State: {self.isFlying}')
        print(f'Battery = {self.battery}')
        print(f'Position = ({self.x},{self.y})')
        print(f'Altitude = {self.altitude}')

    def move(dx, dy, dalt):
        if battery <= 0:
            self.isFlying = False

        self.x += dx
        self.y += dy 
        self.dalt += dalt

        




