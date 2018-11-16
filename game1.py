import pgzrun
import math
import pygame

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
        self.bullet = None
        self.color = color
        self.canfire = True
        self.hp = 10
        
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
        if self.bullet is not None:
            self.bullet.move()
            if not self.bullet.onscreen():
                self.bullet = None

    def fire(self):
        if self.bullet is None and self.canfire == True:
            self.bullet = BulletActor(self.color, self.angle)
            self.bullet.center = self.center
            self.canfire = False
            clock.schedule(self.resetfire , 1.0)

    def resetfire(self):
        self.canfire = True


class BulletActor(TurtleActor):
    def __init__ (self,color,angle):
        super().__init__(color + '_bullet')
        self.angle = angle

    def move(self):
        self.forward(15)

    def onscreen(self):
        screenrect = Rect((0,0), (screen.width, screen.height))
        return screenrect.contains(self._rect)        
        
red_tank = TankActor('red')
red_tank.topleft = 10, 10
blue_tank = TankActor('blue')
blue_tank.bottomright = 490, 490
blue_tank.turnleft (180)
WIDTH = 500
HEIGHT = 500
velocity = 0

def draw():
    screen.blit('arena',(0,0))
    if red_tank.bullet is not None:
        red_tank.bullet.draw()
    if blue_tank.bullet is not None:
        blue_tank.bullet.draw()
    red_tank.draw()
    #draw.rect(screen.surface, red_tank._rect, width=2)
    #screen.rect(, 'white')
    blue_tank.draw()

def update():
    red_tank.move()
    if keyboard[keys.W]:
        if red_tank.velocity <= 5:
            red_tank.velocity += .5
    if keyboard[keys.S]:
        if red_tank.velocity >= -5:
         red_tank.velocity -= .5
    if keyboard[keys.A]:
        red_tank.turnleft(2.5)
    if keyboard[keys.D]:
        red_tank.turnright(2.5)
    if red_tank.bullet is not None:
        rdist = (blue_tank.x - red_tank.bullet.x)**2 + (blue_tank.y - red_tank.bullet.y)**2
        if rdist < 30**2:
            red_tank.bullet = None
    if blue_tank.bullet is not None:
        bdist = (red_tank.x - blue_tank.bullet.x)**2 + (red_tank.y - blue_tank.bullet.y)**2
        if bdist < 30**2:
           blue_tank.bullet = None

    blue_tank.move()
    if keyboard[keys.UP]:
        if blue_tank.velocity <= 5:
            blue_tank.velocity += .5
    if keyboard[keys.DOWN]:
        if blue_tank.velocity >= -5:
         blue_tank.velocity -= .5
    if keyboard[keys.LEFT]:
        blue_tank.turnleft(2.5)
    if keyboard[keys.RIGHT]:
        blue_tank.turnright(2.5)
        
def on_key_down(key):
    if key == keys.E:
        red_tank.fire()
    if key == keys.M:
        blue_tank.fire()

pgzrun.go()
