import pygame
import random
import math
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1600,900))
pygame.display.set_caption('flyer')
clock = pygame.time.Clock()

class Flyer():

    def __init__(self):

        self.left_margin = 200
        self.right_margin = screen.get_width() - 200
        self.top_margin = 200
        self.bottom_margin = screen.get_height() - 200
        self.position = pygame.Vector2(random.randint(self.left_margin, self.right_margin), \
                                       random.randint(self.top_margin, self.bottom_margin))
        self.velocity = pygame.Vector2(random.uniform(-3,3),random.uniform(-3,3))
        self.acceleration = pygame.Vector2(0,0)
        self.mass = 1
        self.top_speed = 8
        self.bottom_speed = 4
        self.surface = pygame.Surface((50,20), pygame.SRCALPHA)
        self.angle = 0
        self.damp = 0.9
    
    def flyer(self, display):

        pygame.draw.polygon(display,'black',((0,0),(display.get_width(),display.get_height()/2),(0,display.get_height())))

    def rotate(self, surface, angle, pivot):

        rotated_image = pygame.transform.rotate(surface, angle)
        rect = rotated_image.get_rect(center=pivot)
        return rotated_image, rect

    def check_edges(self):

        out_of_bounds = False

        if self.position.x > self.right_margin:
            self.velocity.x -= 0.4
            out_of_bounds = True
        
        if self.position.x < self.left_margin:
            self.velocity.x += 0.4
            out_of_bounds = True
        
        if self.position.y < self.top_margin:
            self.velocity.y += 0.4
            out_of_bounds = True

        if self.position.y > self.bottom_margin:
            self.velocity.y -= 0.4
            out_of_bounds = True

        if out_of_bounds:
            self.velocity *= self.damp

    def limit_speed(self):
        if self.velocity.magnitude() > self.top_speed:
            self.velocity.normalize_ip()
            self.velocity *= self.top_speed
    
    def boost_speed(self):
        if self.velocity.magnitude() < self.bottom_speed:
            self.velocity.normalize_ip()
            self.velocity *= self.bottom_speed

    def accel(self):
        accel = self.velocity.copy()
        accel *= 0.15
        self.apply_force(accel)

    def heading(self):
        heading = math.atan2(self.velocity.y, self.velocity.x) * (180/math.pi)
        self.angle = -heading
    
    def apply_force(self, force):
        f = force / self.mass
        self.acceleration += f

    def update(self):
        self.accel()
        self.check_edges()
        self.velocity += self.acceleration
        self.limit_speed()
        self.boost_speed()
        self.position += self.velocity
        
        self.acceleration *= 0

flyer = Flyer()
flyers = []

for i in range(20):
    flyers.append(Flyer())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill('sky blue')

    for i in range(len(flyers)):
        flyers[i].heading()
        rotated_image, rect = flyers[i].rotate(flyers[i].surface, flyers[i].angle, flyers[i].position)
        flyers[i].flyer(flyers[i].surface)
        flyers[i].update()
        screen.blit(rotated_image, rect)

    pygame.display.update()
    clock.tick(60)