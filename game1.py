import pgzrun
import math

class TurtleActor(object):
    def __init__(self, color, *args, **kwargs):
        self.__dict__['_actor'] = Actor(color + '_tank', *args, **kwargs)
        self.velocity = 0
        
    def __getattr__(self, attr):
        if attr in self.__dict__:
            return object.__getattribute__(self, attr)
        else:
            return getattr(self.__dict__['_actor'], attr)
            
    def __setattr__(self, attr, value):
        if attr in self.__dict__:
            return object.__setattribute__(self, attr, value)
        else:
            return setattr(self._actor, attr, value)
        
    def forward(self, distance):
        the_angle = math.radians(self._actor.angle)
        self._actor.x += distance * math.cos(the_angle)
        # We subtract the y as our y gets bigger heading downward
        self._actor.y -= distance * math.sin(the_angle)
        
    def backward(self, distance):
        self.forward(-distance)
        
    def turnleft(self, angle):
        self._actor.angle += angle
    
    def turnright(self, angle):
        self._actor.angle -= angle

    def set_velocity(self, value):
        self.velocity = value

    def move(self):
        self.forward(self.velocity)
        if self.velocity > 0:
            self.velocity /= 1.1
        
red_tank = TurtleActor('red')
red_tank.topright = 0, 10
blue_tank = TurtleActor('blue')
blue_tank.topright = 200, 200
WIDTH = 500
HEIGHT = 500

velocity = 0
def draw():
    screen.clear()
    screen.fill('white')
    red_tank.draw()
    blue_tank.draw()
def update():
    red_tank.move()
    if red_tank.left > WIDTH:
        red_tank.right = 0
    if red_tank.right < 0:
        red_tank.left = WIDTH
    if red_tank.top > HEIGHT:
        red_tank.bottom = 0
    if red_tank.bottom < 0:
        red_tank.top = HEIGHT
        
def on_key_down(key):
    if key == keys.W :
        red_tank.velocity += 5
    if key == keys.A :
        red_tank.turnleft(15)
    if key == keys.D :
        red_tank.turnright(15)
pgzrun.go()
