import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1000,600))
pygame.display.set_caption('Connecting dots')
clock = pygame.time.Clock()

class Circle():

    def __init__(self) -> None:
        self.circle_position = pygame.Vector2(0,0)

    def circle_pos(self, x, y):
        self.circle_position.x = x
        self.circle_position.y = y

    def place_circle(self):
        pygame.draw.circle(screen, 'black', self.circle_position, 5)

class Line():

    def __init__(self) -> None:
        self.line_position_start = pygame.Vector2(0,0)
        self.line_position_end = pygame.Vector2(0,0)

    def line_pos_start(self, x, y):
        self.line_position_start.x = x
        self.line_position_start.y = y

    def line_pos_end(self, x, y):
        self.line_position_end.x = x
        self.line_position_end.y = y

    def place_line(self):
        pygame.draw.line(screen, 'black', self.line_position_start, self.line_position_end)

circles = []
lines = []

while True:

    screen.fill('sky blue')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            circles.append(Circle())
            circles[-1].circle_pos(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

            lines.append(Line())
            num_lines = len(lines)
            if num_lines == 1:
                lines[0].line_pos_start(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            elif num_lines > 1:
                lines[-2].line_pos_end(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                lines[-1].line_pos_start(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

    if len(lines) > 0:
        lines[-1].line_pos_end(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

    for count in range(len(circles)):
        circles[count].place_circle()
        lines[count].place_line()

    pygame.display.update()
    clock.tick(60)
    