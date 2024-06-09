import pygame
import math
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1200,800))

pygame.display.set_caption('Rotation')
clock = pygame.time.Clock()

class Mover():

    def __init__(self):
        self.position = pygame.Vector2(screen.get_width()/2,screen.get_height()/2)
        self.velocity = pygame.Vector2(0,0)
        self.acceleration = pygame.Vector2(0,0)
        self.mass = 1
        self.largestDistance = math.dist((0,0),(1200,900))

        # pygame.SRCALPHA matches the alpha of the surface it is on (makes it transparent)
        self.surface = pygame.Surface((100,40), pygame.SRCALPHA)

        self.topSpeed = 10

    def ply(self,display):
        pygame.draw.polygon(display,'black',((0,0),(display.get_width(),display.get_height()/2),(0,display.get_height())))

    def baton(self, display):
        radius_of_balls = 5
        pygame.draw.line(display, 'white', (radius_of_balls,display.get_height()/2), (display.get_width()-radius_of_balls,display.get_height()/2),2)
        pygame.draw.circle(display,'white', (radius_of_balls,display.get_height()/2), radius_of_balls)
        pygame.draw.circle(display,'white', (display.get_width()-radius_of_balls,display.get_height()/2), radius_of_balls)

    def rotate(self, surface, angle, pivot, offset):
        rotated_image = pygame.transform.rotate(surface, angle)     # -> Surface
        rotated_offset = offset.rotate(angle)                       # -> Vector2
        rect = rotated_image.get_rect(center=pivot+rotated_offset)  # -> rectangle (Rect)
        return rotated_image, rect # -> Surface, rectangle (Rect)
    
    def applyForce(self, force):
        f = force / self.mass
        self.acceleration += f
    
    def update(self):
        self.velocity += self.acceleration
        self.limitSpeed()
        self.position += self.velocity
        self.acceleration *= 0
    
    def goRight(self):
        right = pygame.Vector2(0.01,0)
        self.applyForce(right)
    
    def moveTowardMouse(self):
        position_of_mouse = pygame.Vector2(pygame.mouse.get_pos())
        direction = position_of_mouse - self.position
        distance = direction.magnitude()
        if distance > self.largestDistance:
            distance = self.largestDistance
        magOfAccel = pygame.math.lerp(0.2, 0.1, distance/self.largestDistance)
        direction.normalize_ip()
        direction *= 0.5
        # direction *= magOfAccel
        self.applyForce(direction)
    
    def limitSpeed(self):
        if self.velocity.magnitude() > self.topSpeed:
            self.velocity.normalize_ip()
            self.velocity *= self.topSpeed
    
    def getDirectionAngle(self):
        dir = math.atan2(self.velocity.y, self.velocity.x)
        dir *= (180/math.pi)    # Convert from radians to degrees
        return dir


offset = pygame.math.Vector2(0,0)

obj = Mover()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    angle = -obj.getDirectionAngle()
    pivot = obj.position
    rotated_image, rect = obj.rotate(obj.surface, angle, pivot, offset)
    screen.fill('sky blue')

    obj.ply(obj.surface)

    obj.moveTowardMouse()
    obj.update()
    
    screen.blit(rotated_image, rect)
    
    pygame.display.update()
    clock.tick(60)