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

        self.left_margin = 250
        self.right_margin = screen.get_width() - 250
        self.top_margin = 250
        self.bottom_margin = screen.get_height() - 250
        self.position = pygame.Vector2(random.randint(self.left_margin, self.right_margin), \
                                       random.randint(self.top_margin, self.bottom_margin))
        # self.position = pygame.Vector2(pos_x, pos_y)      # FOR TESTING
        self.velocity = pygame.Vector2(random.uniform(-3,3),random.uniform(-3,3))
        # self.velocity = pygame.Vector2(1,1)               # FOR TESTING
        self.acceleration = pygame.Vector2(0,0)
        self.mass = 1
        self.top_speed = 9
        self.bottom_speed = 1
        self.surface = pygame.Surface((45,18), pygame.SRCALPHA)
        self.angle = 0
        self.damp = 0.95
        self.visible_range = 150
        self.protected_range = 35
        self.avoid = 0.02
        self.match_speed = 0.02
        self.centering = 0.0008
    
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
        accel *= 0.1
        self.apply_force(accel)

    def heading(self):
        heading = math.atan2(self.velocity.y, self.velocity.x) * (180/math.pi)
        self.angle = -heading
    
    def flocking(self, this_boid, boids):

        too_close_x = 0
        too_close_y = 0
        vel_x_avg = 0
        vel_y_avg = 0
        pos_x_avg = 0
        pos_y_avg = 0
        neighbors = 0

        for boid in range(len(boids)):
            if abs(self.position.distance_to(boids[boid].position)) < self.protected_range and this_boid != boid:
                too_close_x += self.position.x - boids[boid].position.x
                too_close_y += self.position.y - boids[boid].position.y
            
            if abs(self.position.distance_to(boids[boid].position)) < self.visible_range and this_boid != boid:
                pos_x_avg += boids[boid].position.x
                pos_y_avg += boids[boid].position.y
                
                vel_x_avg += boids[boid].velocity.x
                vel_y_avg += boids[boid].velocity.y
                
                neighbors += 1

        if neighbors > 0:
            vel_x_avg /= neighbors
            vel_y_avg /= neighbors

            pos_x_avg /= neighbors
            pos_y_avg /= neighbors

        self.velocity.x += too_close_x * self.avoid
        self.velocity.y += too_close_y * self.avoid

        self.velocity.x += (vel_x_avg - self.velocity.x) * self.match_speed
        self.velocity.y += (vel_y_avg - self.velocity.y) * self.match_speed

        self.velocity.x += (pos_x_avg - self.position.x) * self.centering
        self.velocity.y += (pos_y_avg - self.position.y) * self.centering

    def separate(self, this_boid, boids):
        too_close_x = 0
        too_close_y = 0

        for boid in range(len(boids)):
            if abs(self.position.distance_to(boids[boid].position)) < self.protected_range and this_boid != boid:
                too_close_x += self.position.x - boids[boid].position.x
                too_close_y += self.position.y - boids[boid].position.y
        
        self.velocity.x += too_close_x * self.avoid
        self.velocity.y += too_close_y * self.avoid

    def align(self, this_boid, boids):
        vel_x_avg = 0
        vel_y_avg = 0
        neighbors = 0

        for boid in range(len(boids)):
            if abs(self.position.distance_to(boids[boid].position)) < self.visible_range and this_boid != boid:
                vel_x_avg += boids[boid].velocity.x
                vel_y_avg += boids[boid].velocity.y
                neighbors += 1

        if neighbors > 0:
            vel_x_avg /= neighbors
            vel_y_avg /= neighbors

        self.velocity.x += (vel_x_avg - self.velocity.x) * self.match_speed
        self.velocity.y += (vel_y_avg - self.velocity.y) * self.match_speed

    def center(self, this_boid, boids):
        pos_x_avg = 0
        pos_y_avg = 0
        neighbors = 0

        for boid in range(len(boids)):
            if abs(self.position.distance_to(boids[boid].position)) < self.visible_range and this_boid != boid:
                pos_x_avg += boids[boid].position.x
                pos_y_avg += boids[boid].position.y
                neighbors += 1
        
        if neighbors > 0:
            pos_x_avg /= neighbors
            pos_y_avg /= neighbors
        
        self.velocity.x += (pos_x_avg - self.position.x) * self.centering
        self.velocity.y += (pos_y_avg - self.position.y) * self.centering
    
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

# flyer = Flyer()
flyers = []

### FOR TESTING ###
# count = 0
# for i in range(5):
#     flyers.append(Flyer(screen.get_width()/2+count, screen.get_height()/2+count))
#     count += 23

for i in range(80):
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
        flyers[i].flocking(i, flyers)
        flyers[i].update()
        screen.blit(rotated_image, rect)

    pygame.display.update()
    clock.tick(60)