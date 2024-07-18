import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1000,500))
pygame.display.set_caption('Convex Hull Implementation')
clock = pygame.time.Clock()

class Circle():

    def __init__(self) -> None:
        self.circle_position = pygame.Vector2(0,0)

    def circle_pos(self, x, y):
        self.circle_position.x = x
        self.circle_position.y = y

    def place_circle(self):
        pygame.draw.circle(screen, 'black', self.circle_position, 5)

    def flip_y_coord(self):
        # return (int(circle[position].circle_position.x), int(pygame.Surface.get_height() - circle[position].circle_position.y))
        return (int(self.circle_position.x), int(screen.get_height() - self.circle_position.y))

    def calc_slope(self, first_point, point):
        return (point[1] - first_point[1]) / (point[0] - first_point[0])

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

mouse_pressed = False
circles = []
circle_positions = []
lines = []
first_point = (0,0)

while True:

    slopes = []

    # placed_circle = False
    screen.fill('sky blue')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            circles.append(Circle())
            circles[-1].circle_pos(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            # circle_positions.append((int(circles[-1].circle_position.x), int(circles[-1].circle_position.y)))
            circle_positions.append(circles[-1].flip_y_coord())
            circle_pos_dict = dict()
            for pos in range(len(circle_positions)):
                circle_pos_dict[pos] = circle_positions[pos]

            # Initially sorts by y-coordinate then by x-coordinate
            # circle_positions.sort(key=lambda x: (x[1], x[0]))
            first_point = min(circle_positions, key=lambda x: (x[1], x[0]))
            for angle in circle_positions:
                if angle != first_point:
                    slopes.append((angle[1] - first_point[1]) / (angle[0] - first_point[0]))

            # For testing
            print(circle_positions)
            print(circle_pos_dict)
            print(first_point)
            print(slopes)

            lines.append(Line())
            num_lines = len(lines)
            if num_lines == 1:
                lines[0].line_pos_start(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            elif num_lines > 1:
                lines[-2].line_pos_end(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                lines[-1].line_pos_start(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])


    for count in range(len(circles)):
        if count < len(circles) - 1:
            circles[count].place_circle()
            lines[count].place_line()
        
        else:
            circles[count].place_circle()
    
    pygame.display.update()
    clock.tick(60)
    