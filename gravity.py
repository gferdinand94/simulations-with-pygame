import pygame
import random
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1200,900))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

class Mover():

    def __init__(self, x_pos, y_pos, mass):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.mass = mass
        self.radius = self.mass * 2
        self.position = pygame.Vector2(x_pos, y_pos)
        self.velocity = pygame.Vector2(5,-2)
        self.acceleration = pygame.Vector2(0,0)
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)
        self.color = pygame.Color(r,g,b)

    def circle(self, display):
        pygame.draw.circle(display, self.color, self.position, self.radius)
    
    def applyForce(self, force):
        f = force / self.mass
        self.acceleration += f
    
    def update(self):
        self.velocity += self.acceleration
        self.position += self.velocity
        self.acceleration *= 0
    
class Attractor():

    def __init__(self, mass):
        self.mass = mass
        self.radius = mass * 2
        self.x_pos = screen.get_width()/2
        self.y_pos = screen.get_height()/2
        self.position = pygame.Vector2(self.x_pos, self.y_pos)
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)
        self.color = pygame.Color(r,g,b)

    def show(self, display):
        pygame.draw.circle(display, self.color, self.position, self.radius)

    def gravity(self, mover):

        force = self.position - mover.position
        distance = force.magnitude()
        if distance < 5:
            distance = 5
        if distance > 400:
            distance = 400
        mag = (self.mass * mover.mass) / (distance*distance)
        force.normalize()
        force *= mag
        print(distance)
        return force

mover = Mover(screen.get_width() / 3, screen.get_height() / 3, 6)
attractor = Attractor(20)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill('black')

    mover.circle(screen)
    force = attractor.gravity(mover)
    mover.applyForce(force)
    mover.update()
    attractor.show(screen)

    pygame.display.update()
    clock.tick(60)