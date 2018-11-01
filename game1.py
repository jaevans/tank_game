import pgzrun
import math

class TurtleActor(object):
    def __init__(self, *args, **kwargs):
        self.__dict__['_actor'] = Actor(*args, **kwargs)
        
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

        
class TankActor(TurtleActor):
    def __init__(self, color):
        super().__init__(color + '_tank')
        self.velocity = 0

    def set_velocity(self, value):
        self.velocity = value

    def move(self):
        self.forward(self.velocity)
        if self.velocity > 0:
            self.velocity /= 1.1
        if self.velocity < 0:
            self.velocity += .25
        if self.left > WIDTH:
            self.right = 0
        if self.right < 0:
            self.left = WIDTH
        if self.top > HEIGHT:
            self.bottom = 0
        if self.bottom < 0:
            self.top = HEIGHT

class BulletActor(TurtleActor):
    def __init__ (self,color):
        super().__init__(color + '_bullet')

red_tank = TankActor('red')
red_tank.topleft = 10, 10
blue_tank = TankActor('blue')
blue_tank.bottomright = 490, 490
blue_tank.turnleft (180)
WIDTH = 500
HEIGHT = 500
red_bullet = BulletActor('red')
red_bullet.bottomright= 200,200
blue_bullet = BulletActor('blue')
blue_bullet.bottomright = 300,300
velocity = 0

def draw():
    screen.clear()
    screen.fill('white')
    red_bullet.draw()
    blue_bullet.draw()
    red_tank.draw()
    blue_tank.draw()

def update():
    red_tank.move()
    if keyboard[keys.W]:
        if red_tank.velocity <= 10:
            red_tank.velocity += .5
    if keyboard[keys.S]:
        if red_tank.velocity >= -5:
         red_tank.velocity -= .5
    if keyboard[keys.A]:
        red_tank.turnleft(5)
    if keyboard[keys.D]:
        red_tank.turnright(5)

    blue_tank.move()
    if keyboard[keys.UP]:
        if blue_tank.velocity <= 10:
            blue_tank.velocity += .5
    if keyboard[keys.DOWN]:
        if blue_tank.velocity >= -5:
         blue_tank.velocity -= .5
    if keyboard[keys.LEFT]:
        blue_tank.turnleft(5)
    if keyboard[keys.RIGHT]:
        blue_tank.turnright(5)

pgzrun.go()
