import pygame
import random as r
import math as m
from pygame import gfxdraw

# some colours
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

#                               PYGAME INITIAL CONDITIONS
#--------------------------------------------------------------------------------------#
pygame.init()

# screen dimensions
width = 700
height = 600

# Generate random colour. Looks pretty and saves time hardcoding stuff idk
def randColour():
    colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return colour

# set screen size & instantiate
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('N-Body Simulation')

# loop until close
done = False

# screen updates (for readability)
clock = pygame.time.Clock()

# Specific Globals
gravity = (m.pi, 0.002)
drag = 1 # Completely arbitrary, edit at leisure
elasticity = 1 # Completely arbitrary, edit at leisure
#--------------------------------------------------------------------------------------#
#                                   PYGAME OBJECTS
#--------------------------------------------------------------------------------------#
class Particle():
    def __init__(self, x, y, mass, size, angle=0, speed=0):
        self.x = x; self.y = y
        self.mass = mass
        self.size = size
        self.angle = angle
        self.speed = speed

    def display(self):
        try:
            pygame.gfxdraw.filled_circle(screen, int(self.x), int(self.y), self.size, blue)
        except OverflowError:
            pass

    # Speed is a vector and thus can be represented by its direction, determined by it's angle, and its magnitude, which I call speed for simplicities sake:
    def move(self, other):
        force = self.attract(other)
        self.x += m.sin(self.angle) * self.speed
        self.y -= m.cos(self.angle) * self.speed
        return force

    def attract(self, other):
        dx = (self.x - other.x)
        dy = (self.y - other.y)
        dist = m.hypot(dx, dy)
            
        theta = m.atan2(dy, dx)
        force = 0.2 * self.mass * other.mass / dist**2
        try: 
            self.accelerate((theta - 0.5 * m.pi, force/self.mass))
            other.accelerate((theta + 0.5 * m.pi, force/other.mass))
        except ZeroDivisionError:
            pass
        return force

    def accelerate(self, vector):
        self.angle, self.speed = addVectors((self.angle, self.speed), vector)
    
    

#--------------------------------------------------------------------------------------#
#                                DEFINING FUNCTIONS
#--------------------------------------------------------------------------------------#

# Adding angle and length components of vectors together
def addVectors(vector1, vector2):
    a1, l1 = vector1
    a2, l2 = vector2
    x = m.sin(a1) * l1 + m.sin(a2) * l2
    y = m.cos(a1) * l1 + m.cos(a2) * l2
    length = m.hypot(x, y)
    angle = 0.5 * m.pi - m.atan2(y, x)
    return angle, length

# Collision function
def collide(p1, p2):
    # Linear algebra. Who woulda thunk, huh?
    dx = p1.x - p2.x
    dy = p1.y - p2.y

    # math.hypot() saves so much time i love it
    distance = m.hypot(dx, dy)
    if distance < p1.size + p2.size:
        return True

#--------------------------------------------------------------------------------------#
#                               OBJECT INSTANTIATION
#--------------------------------------------------------------------------------------#
sprites = []



# for i in range(10):
#     mass = r.randint(1, 8)
#     # NOTE: Here radius = mass
#     partickle = Particle(r.randint(0 + 50, width - 50), r.randint(0 + 50, height - 50), mass, mass) 
#     sprites.append(partickle)


# x, y, mass, size, angle, speed


# miniguy = Particle(width/3, height-100, 2, 10, 0, .6)
# sprites.append(miniguy)
# Do NOT remove
# dummy = Particle(width+10, height+10, 0, 0)
# sprites.append(dummy)

# centralbody = Particle(width/2, height/2, 1000, 20)
# sprites.append(centralbody)

# Do NOT remove
# dummy = Particle(width+10, height+10, 0.00001, 0)
# sprites.append(dummy)
#--------------------------------------------------------------------------------------#
#                                        MAIN
#--------------------------------------------------------------------------------------#

# Main loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            sprites.append(Particle(200, 0, mass=500, size=10, angle=-m.pi, speed=.1))
            sprites.append(Particle(width - 200, height, mass=500, size=10, angle=0, speed=.1))
            # for i in range(10):
                # miniguy = Particle(r.uniform(0, width), r.uniform(10, height-10), mass=50, size=r.randint(8, 12), angle=r.uniform(0, m.pi), speed=r.uniform(0.10, 0.15))
            # if sprites[0] is dummy:
            #     sprites[0] = miniguy
            # else: sprites.append(miniguy)
            # sprites.append(miniguy)
            # sprites.append(sprites.pop(sprites.index([x for x in sprites if x is dummy][0])))

    # Wipes screen every time to avoid clipping and stuff
    screen.fill(white)

    for i, sprite in enumerate(sprites):
        for particle in sprites:
            if sprite is not particle:
                collided = collide(sprite, particle)
                if collided:
                    if sprite.mass < particle.mass:
                        sprites.remove(sprite)
                    elif sprite.mass == particle.mass:
                        pass
                    else:
                        sprites.remove(particle)
                    # pass
                gForce = sprite.move(particle)
            else: gForce = 0
            # for debugging force: elastic-esque line that shows the force between to centers of mass
            # print(int(gForce*(10**3)))
            print(gForce)

            if sprite or particle is not dummy:
                try:
                    pygame.draw.line(screen, black, (int(sprite.x), int(sprite.y)), (int(particle.x), int(particle.y)), int(m.log2((gForce*(10**3)))))
                except ValueError:
                    pass
                # pygame.draw.line(screen, black, (int(particle.x), int(particle.y)), (int(sprite.x), int(sprite.y)), int(m.log2(gForce*(10**3))))

        sprite.display()

    # Display graphics
    pygame.display.flip()


    clock.tick(120)
