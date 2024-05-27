import pygame
import math
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1200,900))
pygame.display.set_caption('acceleration based on distance from mouse towards mouse')
clock = pygame.time.Clock()

"""
NEED TO FIX LERP FUNCTION:

    - WHEN OBJECT GETS FURTHER FROM MOUSE THAN THE DIAGONAL DISTANCE OF THE
      SCREEN, THE LERP FUNCTION RUNS INTO AN ERROR AND EXITS PROGRAM.
"""
class Mover():

    def __init__(self, color, x_pos, y_pos):
        self.color = color
        # self.x_vel = x_vel
        # self.y_vel = y_vel
        self.position = pygame.Vector2(x_pos, y_pos)
        # self.position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0.0, 0.0)
        self.topSpeed = 13
        self.largestDistance = math.dist((0,0),(1200,900))
    
    def limit(self, vel):
        if vel.magnitude() > self.topSpeed:
            vel.normalize_ip()
            vel *= self.topSpeed

    def accelTowardsMouse(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse = pygame.Vector2(mouse_pos[0], mouse_pos[1])
        direction = mouse - self.position
        distance = direction.magnitude()
        direction.normalize_ip()
        magOfAccel = pygame.math.lerp(0.4, 0.0001, distance/self.largestDistance)
        # self.direction *= 0.2
        direction *= magOfAccel
        self.acceleration = direction
        self.velocity += self.acceleration
        self.limit(self.velocity)
        self.position += self.velocity
    
    def circle(self, display, radius):
        pygame.draw.circle(display, self.color, self.position, radius)
        self.accelTowardsMouse()

cir1 = Mover('purple', 600, 850)
cir2 = Mover('red', 300, 600)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # screen.fill('black')
    screen.fill(pygame.Color(20,50,90, 180))
    # mouse_pos = pygame.mouse.get_pos()
    cir1.circle(screen, 40)
    cir2.circle(screen, 20)
    # print(cir1.magOfAccel)
    # print("Distance",cir1.distance)
    # print("Largest Distance", cir1.largestDistance)
    # print(cir1.velocity.magnitude())


    pygame.display.update()
    clock.tick(60)