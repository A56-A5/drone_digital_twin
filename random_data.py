import random 

class Environment:
    def __init__(self):
        self.weather = random.choice(['windy','rainy','normal'])
        
    
    def randomWind(self):
        if self.weather == 'rainy':
            dx = random.int(-8,8)
            dy = random.int(-8,8)

        wind_direction = random.uniform(-1,1)
        
        dx = random.int(-2,2)
        dy = random.int(-2,2)

        return dx,dy 
    