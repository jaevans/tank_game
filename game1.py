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
        self.bullets = []
        self.color = color
        self.canfire = True
        self.hp = 10.0
        self.speedmult = 1
        self.firedelay = 1.0
        self.confused = False
        self.keys = []
        self.confusedkeys = []
        self.dmg = 1.0 #Damage that the bullet does
        
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
        live_bullets = []
        for new_bullet in self.bullets:
            new_bullet.move()
            if new_bullet.onscreen():
                live_bullets.append(new_bullet)
        self.bullets = live_bullets

    def fire(self):
        if self.canfire == True:
            new_bullet = BulletActor(self.color, self.angle)
            new_bullet.center = self.center
            new_bullet.dmg = self.dmg
            self.canfire = False
            self.bullets.append(new_bullet)
            clock.schedule(self.resetfire , self.firedelay)

    def resetfire(self):
        self.canfire = True

    def damage(self, dmg):
        self.hp -= dmg

    def resetspeed(self):
        self.speedmult = 1

    def resetfiredelay(self):
        self.firedelay = 1.0
        self.dmg = 1.0

    def getkeys(self, confused):
        if confused:
            return self.confusedkeys
        else:
            return self.keys

    def resetconfusion(self):
        self.confused = False

class BulletActor(TurtleActor):
    def __init__ (self,color,angle):
        super().__init__(color + '_bullet')
        self.angle = angle + ((random.random()* 10) - 5)
        self.dmg = 1

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
FIREKEY = 4

class PowerActor(Actor):
    def __init__ (self,power):
        super().__init__(POWER_IMAGES[power])
        self.power = power

red_tank = TankActor('red')
red_tank.topleft = 10, 10
blue_tank = TankActor('blue')
blue_tank.bottomright = 490, 490
blue_tank.turnleft (180)
red_tank.keys = [keys.W, keys.S, keys.A, keys.D, keys.E]
red_tank.confusedkeys = [keys.S, keys.W, keys.D, keys.A, keys.E]
blue_tank.keys = [keys.UP, keys.DOWN, keys.LEFT, keys.RIGHT, keys.M]
blue_tank.confusedkeys = [keys.DOWN, keys.UP, keys.RIGHT, keys.LEFT, keys.M]
WIDTH = 500
HEIGHT = 500
velocity = 0
gameover = False
powerup = None

def draw():
    screen.blit('arena',(0,0))
    for b in red_tank.bullets:
        b.draw()
    for b in blue_tank.bullets:
        b.draw()
    red_tank.draw()
    blue_tank.draw()
    ptext.draw(int(red_tank.hp) == red_tank.hp and "%d" % red_tank.hp or "%0.1f" % red_tank.hp,
               (10,HEIGHT-25), surf=screen.surface,fontsize=30, color='#cc0600', owidth=1, ocolor='#3d85c6')
    ptext.draw(int(blue_tank.hp) == blue_tank.hp and "%d" % blue_tank.hp or "%0.1f" % blue_tank.hp,
               (WIDTH-35, 5), surf=screen.surface,fontsize=30, color='#3d85c6', owidth=1, ocolor='#cc0600')
    if gameover:
        if blue_tank.hp <= 0:
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
    mykeys = red_tank.getkeys(blue_tank.confused)
    if keyboard[mykeys[FWDKEY]]:
        if red_tank.velocity <= 5 * red_tank.speedmult:
            red_tank.velocity += .5 * red_tank.speedmult
    if keyboard[mykeys[BACKKEY]]:
        if red_tank.velocity >= -5 * red_tank.speedmult:
         red_tank.velocity -= .5 * red_tank.speedmult
    if keyboard[mykeys[LEFTKEY]]:
        red_tank.turnleft(2.5)
    if keyboard[mykeys[RIGHTKEY]]:
        red_tank.turnright(2.5)
    if keyboard[mykeys[FIREKEY]]:
        red_tank.fire()
    uncollided_bullets = []
    for b in red_tank.bullets:
        rdist = distance(blue_tank, b)
        if rdist < 30**2:
            blue_tank.damage(b.dmg)
            if blue_tank.hp <= 0:
                gameover = True
        else:
            uncollided_bullets.append(b)
    red_tank.bullets = uncollided_bullets
    uncollided_bullets = []
            
    blue_tank.move()
    mykeys = blue_tank.getkeys(red_tank.confused)
    if keyboard[mykeys[FWDKEY]]:
        if blue_tank.velocity <= 5 * blue_tank.speedmult:
            blue_tank.velocity += .5 * blue_tank.speedmult
    if keyboard[mykeys[BACKKEY]]:
        if blue_tank.velocity >= -5 * blue_tank.speedmult: 
         blue_tank.velocity -= .5 * blue_tank.speedmult
    if keyboard[mykeys[LEFTKEY]]:
        blue_tank.turnleft(2.5)
    if keyboard[mykeys[RIGHTKEY]]:
        blue_tank.turnright(2.5)
    if keyboard[mykeys[FIREKEY]]:
        blue_tank.fire()
    for b in blue_tank.bullets:
        bdist = distance(red_tank, b)
        if bdist < 30**2:
           red_tank.damage(b.dmg)
           if red_tank.hp <= 0:
                gameover = True
        else:
            uncollided_bullets.append(b)
    blue_tank.bullets = uncollided_bullets
    uncollided_bullets = []
    
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
                        clock.schedule (tank.resetfiredelay, 2.5)
                        tank.dmg = 0.5
                    elif powerup.power == CONFUSION:
                        tank.confused = True
                        clock.schedule (tank.resetconfusion, 10)
                    powerup = None
                    break

def distance(p1, p2):
    return (p1.x-p2.x)**2 + (p1.y-p2.y)**2

POWERDELAY = 5.0

def createpower():
    if not gameover == True:
        global powerup
        powerup = PowerActor(random.randint(RAPID, RAPID))
        clock.schedule(createpower , POWERDELAY)
        powerup.center = (random.randint(64, WIDTH-64), random.randint(64,HEIGHT-64))

clock.schedule(createpower , POWERDELAY)

pgzrun.go()
