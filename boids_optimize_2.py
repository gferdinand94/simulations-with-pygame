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

        self.left_margin = 150
        self.right_margin = screen.get_width() - 150
        self.top_margin = 150
        self.bottom_margin = screen.get_height() - 150
        self.position = pygame.Vector2(random.randint(self.left_margin, self.right_margin), \
                                       random.randint(self.top_margin, self.bottom_margin))
        # self.position = pygame.Vector2(pos_x, pos_y)      # FOR TESTING
        self.velocity = pygame.Vector2(random.uniform(-5,5),random.uniform(-5,5))
        # self.velocity = pygame.Vector2(1,1)               # FOR TESTING
        self.acceleration = pygame.Vector2(0,0)
        self.mass = 1
        self.top_speed = 4
        self.bottom_speed = 2
        self.surface = pygame.Surface((15,7), pygame.SRCALPHA)
        self.angle = 0
        self.damp = 0.95
        self.visible_range = 100
        self.protected_range = 15
        self.avoid = 0.025
        self.match_speed = 0.03
        self.centering = 0.0007

        self.resolution = 20
        self.total_rows = math.floor(screen.get_height() / self.resolution)
        self.total_cols = math.floor(screen.get_width() / self.resolution)

    def draw_grid(self):
        for i in range(0,screen.get_height(),self.resolution):
            pygame.draw.line(screen,'dark grey',(0,i),(screen.get_width(),i))
        for i in range(0,screen.get_width(),self.resolution):
            pygame.draw.line(screen,'dark grey',(i,0),(i,screen.get_height()))

    def get_row(self):
        row = math.floor(self.position.y / self.resolution)
        if row < 0:
            return 0
        if row >= self.total_rows:
            return self.total_rows-1
        return row
    
    def get_col(self):
        col = math.floor(self.position.x / self.resolution)
        if col < 0:
            return 0
        if col >= self.total_cols:
            return self.total_cols-1
        return col
    
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
    
    def flocking(self, this_boid, grid):

        too_close_x = 0
        too_close_y = 0
        vel_x_avg = 0
        vel_y_avg = 0
        pos_x_avg = 0
        pos_y_avg = 0
        neighbors = 0

        neighbors_list = []
        for i in range(-1,2):
            next_row = self.get_row() + i
            for j in range(-1,2):
                next_col = self.get_col() + j

                if next_row >= 0 and next_row < self.total_rows and next_col >= 0 and next_col < self.total_cols:
                    neighbors_list.extend(grid[next_col][next_row])

        for boid in range(len(neighbors_list)):
            if abs(self.position.distance_to(neighbors_list[boid].position)) < self.protected_range and this_boid != boid:
                too_close_x += self.position.x - neighbors_list[boid].position.x
                too_close_y += self.position.y - neighbors_list[boid].position.y
            
            if abs(self.position.distance_to(neighbors_list[boid].position)) < self.visible_range and this_boid != boid:
                pos_x_avg += neighbors_list[boid].position.x
                pos_y_avg += neighbors_list[boid].position.y
                
                vel_x_avg += neighbors_list[boid].velocity.x
                vel_y_avg += neighbors_list[boid].velocity.y
                
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

# class Flock():

#     def __init__(self):
#         self.boids = []
    
#     def add_boid(self, boid):
#         self.boids.append(boid)
    
#     def run(self):
#         for boid in range(len(self.boids)):
#             self.boids[boid].flocking(boid, self.boids)
        
flyers = []

for i in range(500):
    flyers.append(Flyer())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill('sky blue')

    resolution = 20
    rows = math.floor(screen.get_height() / resolution)
    cols = math.floor(screen.get_width() / resolution)

    grid = [[[] for i in range(rows)] for i in range(cols)]

    # Add flyers/boids to the appropriate cells in the grid where they are currently located
    for i in range(len(flyers)):
        grid[flyers[i].get_col()][flyers[i].get_row()].append(flyers[i])
        
    for i in range(len(flyers)):
        flyers[i].heading()
        rotated_image, rect = flyers[i].rotate(flyers[i].surface, flyers[i].angle, flyers[i].position)
        flyers[i].flyer(flyers[i].surface)
        flyers[i].flocking(i, grid)
        flyers[i].update()
        screen.blit(rotated_image, rect)
    
    # flyers[0].draw_grid()
    
    pygame.display.update()
    clock.tick(60)