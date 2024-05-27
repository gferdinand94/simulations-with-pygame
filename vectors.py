import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Bouncing ball with acceleration using vectors')
clock = pygame.time.Clock()

class Mover():

    def __init__(self, color, x_vel, y_vel) -> None:
        self.position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        self.color = color
        self.velocity = pygame.Vector2(x_vel, y_vel)
        self.acceleration = pygame.Vector2(0.0, 0.09)         # Predefined acceleration constant
        self.topSpeed = 10
    
    # def checkEdges(self, x_pos, y_pos):
    #     if x_pos > screen.get_width() or x_pos < 0:
    #         self.velocity.x *= -1
    #     if y_pos > screen.get_height() or y_pos < 0:
    #         self.velocity.y *= -1

    def checkEdges(self):
        if self.position.x > screen.get_width():
            self.position.x = screen.get_width()        # reset position
            self.velocity.x *= -1
        if self.position.x < 0:
            self.position.x = 0                         # reset position
            self.velocity.x *= -1

        if self.position.y > screen.get_height():
            self.position.y = screen.get_height()       # reset position
            self.velocity.y *= -1
        if self.position.y < 0:
            self.position.y = 0                         # reset position
            self.velocity.y *= -1

    def teleport(self):
        if self.position.x < 0:
            self.position.x = screen.get_width()
        elif self.position.x > screen.get_width():
            self.position.x = 0

        if self.position.y < 0:
            self.position.y = 400
        elif self.position.y > screen.get_height():
            self.position.y = 0

    def limit(self, vel):
        if vel.magnitude() > self.topSpeed:
            vel.normalize_ip()
            vel *= self.topSpeed

    def update(self):
        self.velocity += self.acceleration
        self.limit(self.velocity)
        self.position += self.velocity

    def circle(self, display, radius, animate):
        pygame.draw.circle(display, self.color, self.position, radius)

        if animate:
            self.update()

        # self.checkEdges()
        # self.checkEdges(self.position.x, self.position.y)
        # self.teleport()

circle1 = Mover('purple', 2, 0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill('white')
    circle1.circle(screen, 40, True)
    circle1.checkEdges()
    # circle1.teleport()
    # print(circle1.velocity.magnitude())
    print(circle1.position.y)
    pygame.display.update()
    clock.tick(80)
    