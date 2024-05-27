"""
FORCES ARE APPLIED TO AN OBJECT. SIMULATION STARTS BY IMPOSING A GRAVITY FORCE
ON THE OBJECT. THE USER CAN USE THE CLICK AND HOLD THE MOUSE TO APPLY A 'WIND' 
FORCE.
"""

import pygame
import random
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,800))
pygame.display.set_caption('Forces')
clock = pygame.time.Clock()

class Mover():

    def __init__(self, x_pos, y_pos, color, radius, cf):
        self.position = pygame.Vector2(x_pos, y_pos)
        self.velocity = pygame.Vector2(0,0)
        self.acceleration = pygame.Vector2(0,0)
        self.mass = radius * 0.4
        self.color = color
        self.radius = radius
        self.cf = cf            # Coefficient of friction
        # self.rect = pygame.Rect(self.position.x, self.position.y, 40, 40)
        self.sideLength = 80
        self.sideHeight = 40
        self.sideDepth = 10

    def checkEdges(self):
        bounce = -0.3           # emulate loss of kinetic energy to inelastic collisions
        if self.position.x > screen.get_width() - self.radius:
            self.position.x = screen.get_width() - self.radius  # reset position
            self.velocity.x *= bounce
        if self.position.x < 0 + self.radius:
            self.position.x = 0 + self.radius                   # reset position
            self.velocity.x *= bounce

        if self.position.y > screen.get_height() - self.radius:
            self.position.y = screen.get_height() - self.radius # reset position
            self.velocity.y *= bounce
        if self.position.y < 0 + self.radius:
            self.position.y = 0 + self.radius                   # reset position
            self.velocity.y *= bounce

    def contactingEdge(self):
        return self.position.y > screen.get_height() - self.radius - 1
    
    def propel(self):
        randX = random.uniform(-1,1) * 100          # propel in x direction
        randY = random.uniform(-1,-0.5) * 100              # propel in y direction
        propelObject = pygame.Vector2(randX, randY)
        self.velocity *= 0.01
        self.applyForce(propelObject)
    
    def friction(self):
        mu = self.cf        # Coefficient of friction
        normal = 1          # Magnitude of normal vector
        
        if self.contactingEdge():
            friction = self.velocity.copy()
            friction *= -1*mu*normal
            self.applyForce(friction)

    def applyForce(self, force):
        f = force / self.mass
        self.acceleration += f

    def circle(self, display):
        pygame.draw.circle(display, self.color, self.position, self.radius)

    def rectangle(self, display):

        pygame.draw.rect(display, self.color, pygame.Rect(self.position.x, self.position.y, self.sideLength, self.sideHeight))

    def update(self):
        self.velocity += self.acceleration
        self.position += self.velocity
        self.acceleration *= 0
        self.checkEdges()

class Liquid(Mover):

    def __init__(self, w, h, offsetX, offsetY, c, mover):
        self.w = w              # 800
        self.h = h              # 200
        self.offsetX = offsetX  # 0
        self.offsetY = screen.get_height() - offsetY  # 200
        self.c = c
        self.sideLength = mover.sideLength
        self.sideHeight = mover.sideHeight
        self.sideDepth = mover.sideDepth
    
    def show(self):
        waterColor = pygame.Color(10,50,100)
        self.surface = pygame.Surface((self.w, self.h))
        self.surface.fill(waterColor)
        self.surface.set_alpha(120)     # make water slightly transparent
        screen.blit(self.surface,(self.offsetX,self.offsetY))

    def contains(self, object):
        return object.position.x >= self.offsetX and object.position.y <= self.w and \
               object.position.y >= self.offsetY and object.position.y <= self.h + self.offsetY
    
    def calcDrag(self, object):
        velSquared = object.velocity.magnitude_squared()
        dragForce = object.velocity.copy()
        vel = dragForce.magnitude()
        area = self.sideLength * self.sideDepth
        if object.velocity.x != 0 or object.velocity.y != 0:
            dragForce.normalize_ip()
        dragMag = vel*vel*self.c * area
        if dragMag >= vel:
            dragForce *= -1*(vel*vel)
        else:
            dragForce *= -1*vel*vel*self.c * area

        return dragForce

circle1 = Mover(screen.get_width() / 2, 0, pygame.Color(180, 40, 90), 30, 0.1)
circle2 = Mover(screen.get_width()// 3, 0, pygame.Color(25, 175, 60), 60, 0.2)

rect1 = Mover(screen.get_width() / 2, 0, pygame.Color(180, 40, 90), 30, 0.1)
rect2 = Mover(screen.get_width()// 4, 0, pygame.Color(25, 175, 60), 60, 0.2)

liquid = Liquid(800,200,0,200,0.2, rect1)
mouse_pressed = False

"""
ANIMATION LOOP
"""
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # circle1.propel()
            # circle2.propel()
            mouse_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pressed = False
        
    if mouse_pressed:
        wind_force = pygame.Vector2(1.5, 0)
        # circle1.applyForce(wind_force)
        # circle2.applyForce(wind_force)

    screen.fill(pygame.Color(60,90,110))
    
    # if liquid.contains(circle1):
    #     drag_force_1 = liquid.calcDrag(circle1)
    #     circle1.applyForce(drag_force_1)
    
    # if liquid.contains(circle2):
    #     drag_force_2 = liquid.calcDrag(circle2)
    #     circle2.applyForce(drag_force_2)

    if liquid.contains(rect1):
        drag_force_1 = liquid.calcDrag(rect1)
        rect1.applyForce(drag_force_1)
        
    # if liquid.contains(rect2):
    #     drag_force_2 = liquid.calcDrag(rect2)
    #     rect1.applyForce(drag_force_2)
    
    gravity_force = pygame.Vector2(0, 0.3)

    # circle1.circle(screen)
    # circle1.applyForce(gravity_force * circle1.mass)
    # circle1.friction()
    # circle1.update()

    # circle2.circle(screen)
    # circle2.applyForce(gravity_force * circle2.mass)
    # circle2.friction()
    # circle2.update()

    rect1.rectangle(screen)
    rect1.applyForce(gravity_force * rect1.mass)
    rect1.friction()
    rect1.update()

    # rect2.rectangle(screen)
    # rect2.applyForce(gravity_force * rect2.mass)
    # rect2.friction()
    # rect2.update()

    liquid.show()
    pygame.display.update()
    clock.tick(60)