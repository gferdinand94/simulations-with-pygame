import pygame
import math
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1200,800))
pygame.display.set_caption('Pendulum')
clock = pygame.time.Clock()

class Rotator():

    def __init__(self):
        self.position = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)
        self.r = screen.get_height() * 0.25
        self.theta = 90
    
    def deg_to_rad(self, angle):

        return angle * (math.pi/180)

rot = Rotator()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill('black')

    pos_x = rot.r * math.cos(rot.deg_to_rad(rot.theta))
    pos_y = rot.r * math.sin(rot.deg_to_rad(rot.theta))

    pygame.draw.line(screen,'white', rot.position, (rot.position.x + pos_x, rot.position.y + pos_y))
    pygame.draw.circle(screen,'white', (rot.position.x + pos_x, rot.position.y + pos_y), 20)

    rot.theta += 2

    pygame.display.update()
    clock.tick(60)