import pygame
import math
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1200,800))

pygame.display.set_caption('spaceship')
clock = pygame.time.Clock()

class Mover():

    def __init__(self):
        self.position = pygame.Vector2(screen.get_width()/2,screen.get_height()/2)
        self.velocity = pygame.Vector2(0,0)
        self.acceleration = pygame.Vector2(0,0)
        self.mass = 1
        self.largestDistance = math.dist((0,0),(1200,900))
        self.angle = 0
        self.damp = 0.995

        # pygame.SRCALPHA matches the alpha of the surface it is on (makes it transparent)
        self.surface = pygame.Surface((100,40), pygame.SRCALPHA)

        self.topSpeed = 14

    def ply(self,display):
        pygame.draw.polygon(display,'black',((0,0),(display.get_width(),display.get_height()/2),(0,display.get_height())))

    def car(self,display):
        car = pygame.Rect(0,0,display.get_width(),display.get_height())
        front = pygame.Rect(display.get_width()-display.get_width()/4, \
                            0, \
                            display.get_width()/4, \
                            display.get_height())
        
        pygame.draw.rect(display,'black',car)
        pygame.draw.rect(display,'forest green',front)

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
        self.velocity *= self.damp
        self.limitSpeed()
        self.position += self.velocity
        self.wrapEdges()
        self.acceleration *= 0

    def turnRight(self):
        self.angle -= 2

    def turnLeft(self):
        self.angle += 2

    def brake(self):
        brake = self.velocity.copy()
        if brake != (0,0):
            brake.normalize_ip()
        brake *= -1 * self.velocity.magnitude() / 16
        self.applyForce(brake)
    
    def accel(self):
        accel = self.velocity.copy()
        mag = 0.15
        ang = -self.angle * (math.pi/180)
        accel.x = math.cos(ang) * mag
        accel.y = math.sin(ang) * mag
        self.applyForce(accel)
    
    def limitSpeed(self):
        if self.velocity.magnitude() > self.topSpeed:
            self.velocity.normalize_ip()
            self.velocity *= self.topSpeed
    
    def getDirectionAngle(self):
        dir = math.atan2(self.velocity.y, self.velocity.x)
        dir *= (180/math.pi)    # Convert from radians to degrees
        return dir
    
    def reset(self):
        self.position = pygame.Vector2(screen.get_width()/2,screen.get_height()/2)
        self.velocity = pygame.Vector2(0,0)

    def wrapEdges(self):
        if self.position.x < 0:
            self.position.x = screen.get_width()
        if self.position.x > screen.get_width():
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = screen.get_height()
        if self.position.y > screen.get_height():
            self.position.y = 0


offset = pygame.math.Vector2(0,0)

obj = Mover()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        obj.turnLeft()
    if keys[pygame.K_d]:
        obj.turnRight()
    if keys[pygame.K_SPACE]:
        obj.brake()
    if keys[pygame.K_k]:
        obj.accel()
    if keys[pygame.K_r]:
        obj.reset()

    pivot = obj.position
    rotated_image, rect = obj.rotate(obj.surface, obj.angle, pivot, offset)
    screen.fill('sky blue')

    obj.ply(obj.surface)

    obj.update()
    
    screen.blit(rotated_image, rect)
    
    pygame.display.update()
    clock.tick(60)