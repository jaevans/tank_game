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
    #screen.blit('arena',(0,0))
    screen.fill('white')
    if red_tank.bullet is not None:
        red_tank.bullet.draw()
    if blue_tank.bullet is not None:
        blue_tank.bullet.draw()
    red_tank.draw()
    pygame.draw.rect(screen.surface, pygame.Color('black'), red_tank._rect, 2)
    #screen.rect(, 'white')
    blue_tank.draw()
    pygame.draw.rect(screen.surface, pygame.Color('black'), blue_tank._rect, 2)

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
    if keyboard[keys.E]:
        if red_tank.bullet is None:
            red_tank.bullet = BulletActor('red', red_tank.angle)
            red_tank.bullet.center = red_tank.center
    if red_tank.bullet is not None:
        if red_tank.bullet._rect.colliderect(blue_tank._rect):
            red_tank.bullet = None
    if blue_tank.bullet is not None:
        if blue_tank.bullet._rect.colliderect(red_tank._rect):
            blue_tank.bullet = None

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
    if keyboard[keys.M]:
        if blue_tank.bullet is None:
            blue_tank.bullet = BulletActor('blue', blue_tank.angle)
            blue_tank.bullet.center = blue_tank.center
        

pgzrun.go()
