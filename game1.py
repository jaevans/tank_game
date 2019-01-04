import pgzrun
import math
import pygame
import ptext
import random

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
        self.speedmult = 1
        self.firedelay = 1.0
        self.keys = []
        
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
            clock.schedule(self.resetfire , self.firedelay)

    def resetfire(self):
        self.canfire = True

    def damage(self):
        self.hp -= 1

    def resetspeed(self):
        self.speedmult = 1

    def resetfiredelay(self):
        self.firedelay = 1.0

class BulletActor(TurtleActor):
    def __init__ (self,color,angle):
        super().__init__(color + '_bullet')
        self.angle = angle

    def move(self):
        self.forward(15)

    def onscreen(self):
        screenrect = Rect((0,0), (screen.width, screen.height))
        return screenrect.contains(self._rect)        

HEALTH = 1
SPEED = 2
RAPID = 3
CONFUSION = 4

POWER_IMAGES = {
    HEALTH: 'health',
    SPEED: 'speed',
    RAPID: 'rapid',
    CONFUSION: 'confusion',
    }

FWDKEY = 0
BACKKEY = 1
LEFTKEY = 2
RIGHTKEY = 3

class PowerActor(Actor):
    def __init__ (self,power):
        super().__init__(POWER_IMAGES[power])
        self.power = power

red_tank = TankActor('red')
red_tank.topleft = 10, 10
blue_tank = TankActor('blue')
blue_tank.bottomright = 490, 490
blue_tank.turnleft (180)
red_tank.keys = [keys.W, keys.S, keys.A, keys.D]
blue_tank.keys = [keys.UP, keys.DOWN, keys.LEFT, keys.RIGHT]
WIDTH = 500
HEIGHT = 500
velocity = 0
gameover = False
powerup = None

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
    ptext.draw(str(red_tank.hp), (10,HEIGHT-25), surf=screen.surface,fontsize=30, color='#cc0600', owidth=1, ocolor='#3d85c6')
    ptext.draw(str(blue_tank.hp), (WIDTH-35, 5), surf=screen.surface,fontsize=30, color='#3d85c6', owidth=1, ocolor='#cc0600')
    if gameover:
        if blue_tank.hp == 0:
            ptext.draw('RED VICTORY', center=(WIDTH/2, HEIGHT/2), align='center', surf=screen.surface,fontsize=60, color='#cc0600', owidth=1, ocolor='#3d85c6')
        else:
            ptext.draw('BLUE VICTORY', center=(WIDTH/2, HEIGHT/2), align='center', surf=screen.surface,fontsize=60, color='#3d85c6', owidth=1, ocolor='#cc0600')
    if powerup:
        powerup.draw()

def update():
    global gameover
    global powerup
    if gameover:
        return
    red_tank.move()
    if keyboard[keys.W]:
        if red_tank.velocity <= 5 * red_tank.speedmult:
            red_tank.velocity += .5 * red_tank.speedmult
    if keyboard[keys.S]:
        if red_tank.velocity >= -5 * red_tank.speedmult:
         red_tank.velocity -= .5 * red_tank.speedmult
    if keyboard[keys.A]:
        red_tank.turnleft(2.5)
    if keyboard[keys.D]:
        red_tank.turnright(2.5)
    if red_tank.bullet is not None:
        rdist = distance(blue_tank, red_tank.bullet)
        if rdist < 30**2:
            red_tank.bullet = None
            blue_tank.damage()
            if blue_tank.hp == 0:
                gameover = True
            
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
    if blue_tank.bullet is not None:
        bdist = distance(red_tank, blue_tank.bullet)
        if bdist < 30**2:
           blue_tank.bullet = None
           red_tank.damage()
           if red_tank.hp == 0:
                gameover = True

    if powerup is not None:
        for tank in [red_tank, blue_tank]:
            rpowerdist = distance(tank, powerup)
            if rpowerdist < 30**2:
                    if powerup.power == HEALTH:
                        tank.hp = tank.hp + 3
                        if tank.hp > 10:
                           tank.hp = 10
                    elif powerup.power == SPEED:
                        tank.speedmult = 2
                        clock.schedule(tank.resetspeed, 10)
                    elif powerup.power == RAPID:
                        tank.firedelay = 0.1
                        clock.schedule (tank.resetfiredelay, 5)
                    elif powerup.power == CONFUSION:
                        pass
                    powerup = None
                    break
            
def on_key_down(key):
    if key == keys.E:
        red_tank.fire()
    if key == keys.M:
        blue_tank.fire()

def distance(p1, p2):
    return (p1.x-p2.x)**2 + (p1.y-p2.y)**2

POWERDELAY = 5.0

def createpower():
    global powerup
    powerup = PowerActor(random.randint(HEALTH, CONFUSION))
    clock.schedule(createpower , POWERDELAY)
    powerup.center = (random.randint(64, WIDTH-64), random.randint(64,HEIGHT-64))

clock.schedule(createpower , POWERDELAY)

pgzrun.go()
