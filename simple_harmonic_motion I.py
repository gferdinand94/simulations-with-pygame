import pygame
import math
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1200,800))
pygame.display.set_caption('Simple Harmonic Motion (Sine Waves)')
clock = pygame.time.Clock()

class Rotator():

    def __init__(self, x_pos, y_pos):
        self.pivot = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)
        # self.position = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)
        self.position = pygame.Vector2(x_pos, y_pos)
        self.r = screen.get_height() * 0.4
        self.theta = 90
        self.framecount = 0
        self.radius = 0
    
    def deg_to_rad(self, angle):

        return angle * (math.pi/180)

    def oscillate(self, r, framecount):
        amplitude = r
        period = 140
    
        return amplitude * math.sin(math.pi * 2 * framecount / period)
    
    def remap(self, value, start1, stop1, start2, stop2):
        new_value = (value - start1) / (stop1 - start1) * (stop2 - start2) + start2
        return new_value

# rot = Rotator()
rot_objects = []
num_objects = 60
next_dist_x = screen.get_width() - screen.get_height()
dist_between_y = screen.get_height() / num_objects
next_dist_y = 20
framecount = 0

for i in range(num_objects):

    rot_objects.append(Rotator(next_dist_x, next_dist_y))
    next_dist_y += dist_between_y
    next_dist_x += 20


start_angle = 0
angle_velocity = 0.2
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill('black')

    angle = start_angle
    start_angle += 0.02

    next_dist_x = screen.get_width() - screen.get_height()
    for i in range(len(rot_objects)):

        pos_x = rot_objects[i].oscillate(rot_objects[i].r, framecount)
        x = rot_objects[i].remap(math.sin(angle), -1, 1, 100, screen.get_width()-100)
        pygame.draw.circle(screen,'white', (x, rot_objects[i].position.y), 20)
        angle += angle_velocity
        
    framecount += 1

    pygame.display.update()
    clock.tick(60)