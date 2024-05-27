"""
FORCES ARE APPLIED TO AN OBJECT. SIMULATION STARTS BY IMPOSING A GRAVITY FORCE
ON THE OBJECT. THE USER CAN USE THE CLICK AND HOLD THE MOUSE TO APPLY A 'WIND' 
FORCE.
"""

import pygame
import random
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Forces')
clock = pygame.time.Clock()

class Mover():

    def __init__(self, x_pos, y_pos, mass, color, radius, cf):
        self.position = pygame.Vector2(x_pos, y_pos)
        self.velocity = pygame.Vector2(0,0)
        self.acceleration = pygame.Vector2(0,0)
        self.mass = mass
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
    
    def friction(self):
        mu = self.cf        # Coefficient of friction
        normal = 1          # Magnitude of normal vector
        
        if self.contactingEdge():
            friction = self.velocity.copy()
            friction *= -1*mu*normal
            self.applyForce(friction)
    
    def propel(self):
        randX = random.uniform(-1,1) * 100          # propel in x direction
        randY = random.uniform(-1,-0.5) * 100              # propel in y direction
        propelObject = pygame.Vector2(randX, randY)
        self.velocity *= 0
        self.applyForce(propelObject)


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

circle1 = Mover(screen.get_width() / 2, 0, 10, pygame.Color(180, 40, 90), 30, 0.1)
circle2 = Mover(screen.get_width()// 3, 0, 30, pygame.Color(25, 175, 60), 60, 0.2)
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
            circle1.propel()
            mouse_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pressed = False
        
    if mouse_pressed:
        wind_force = pygame.Vector2(1.5, 0)
        # circle1.applyForce(wind_force)
        circle2.applyForce(wind_force)

    screen.fill(pygame.Color(60,90,110))

    gravity_force = pygame.Vector2(0, 0.3)

    circle1.circle(screen)
    circle1.applyForce(gravity_force * circle1.mass)
    circle1.friction()
    circle1.update()

    circle2.circle(screen)
    circle2.applyForce(gravity_force * circle2.mass)
    circle2.friction()
    circle2.update()

    pygame.display.update()
    clock.tick(60)