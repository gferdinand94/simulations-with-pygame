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
        self.mass = radius * 0.04
        self.color = color
        self.radius = radius
        self.cf = cf            # Coefficient of friction

    def checkEdges(self):
        bounce = -0.9           # emulate loss of kinetic energy to inelastic collisions
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
        randX = random.uniform(-1,1) * 5          # propel in x direction
        randY = random.uniform(-1,-0.5) * 5              # propel in y direction
        propelObject = pygame.Vector2(randX, randY)
        self.velocity *= 0
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

    def update(self):
        self.velocity += self.acceleration
        self.position += self.velocity
        self.acceleration *= 0
        self.checkEdges()

class Liquid:

    def __init__(self, w, h, offsetX, offsetY, c):
        self.w = w              # 800
        self.h = h              # 200
        self.offsetX = offsetX  # 0
        self.offsetY = screen.get_height() - offsetY  # 200
        self.c = c
    
    def show(self):
        waterColor = pygame.Color(40,50,100)
        self.surface = pygame.Surface((self.w, self.h))
        self.surface.fill(waterColor)
        self.surface.set_alpha(120)     # make water slightly transparent
        screen.blit(self.surface,(self.offsetX,self.offsetY))

    def contains(self, object):
        return object.position.x >= self.offsetX and object.position.y <= self.w and \
               object.position.y >= self.offsetY and object.position.y <= self.h + self.offsetY
    
    def calcDrag(self, object):
        # vel = object.velocity.magnitude()
        dragForce = object.velocity.copy()
        vel = dragForce.magnitude()
        if object.velocity.x != 0 or object.velocity.y != 0:
            dragForce.normalize_ip()
        dragMagnitude = vel*vel*self.c
        if dragMagnitude >= vel:
            dragForce *= -1*(vel/2)
        else:
            dragForce *= -1*vel*vel*self.c
        # dragForce *= -1*vel*vel*self.c

        return dragForce
    
    def limit(self, velocity):
        if velocity.magnitude() > self.topSpeed:
            velocity.normalize_ip()
            velocity *= self.topSpeed


circles = []
liquid = Liquid(800,200,0,200,0.15)

for i in range(7):
    radii = random.randint(10,50)
    c1 = random.randint(1,255)
    c2 = random.randint(1,255)
    c3 = random.randint(1,255)
    circles.append(Mover(100+i*100, 0, pygame.Color(c1, c2, c3), radii, 0.1))

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
            for circle in circles:
                circle.propel()

            mouse_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pressed = False

    screen.fill(pygame.Color(60,90,110))

    for circle in range(len(circles)):
        if liquid.contains(circles[circle]):
            drag_force = liquid.calcDrag(circles[circle])
            circles[circle].applyForce(drag_force)

        gravity_force = pygame.Vector2(0,0.3)
        circles[circle].circle(screen)
        circles[circle].applyForce(gravity_force * circles[circle].mass)
        circles[circle].friction()
        circles[circle].update()

    liquid.show()
    pygame.display.update()
    clock.tick(60)