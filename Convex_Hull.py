import pygame
import math
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1600,900))
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
        pygame.draw.line(screen, 'black', self.line_position_start, self.line_position_end, 2)

def counterclockwise(p1, p2, p3):
    return ((p2[0]-p1[0]) * (p3[1]-p1[1])) - ((p2[1]-p1[1]) * (p3[0]-p1[0]))

def flip(y):
        return int(screen.get_height() - y)

circles = []
circle_positions = []
lines = []
first_point = (0,0)
clicks = 0
circle_pos_dict = dict()
# slopes = []
slopes_sorted = []

while True:

    slopes = []
    slopes_dict = dict()
    points_sorted_by_angle = []
    stack = []
    stack_draw = []

    # placed_circle = False
    screen.fill('sky blue')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:

            lines = []

            # When clicking, add a Circle object
            circles.append(Circle())

            # Give the current Circle object a position (current position of the mouse)
            circles[-1].circle_pos(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

            # Add circle positions in adjusted coordinates
            circle_positions.append(circles[-1].flip_y_coord())

            # Keep track of circle positions
            circle_pos_dict[clicks] = circle_positions[clicks]

            # Initially sorts by y-coordinate then by x-coordinate
            # circle_positions.sort(key=lambda x: (x[1], x[0]))

            # Finds the bottom left-most point by finding the point with the lowest y-value and then if
            # two points have the same lowest y-value, sort by the lowest x-value
            first_point = min(circle_positions, key=lambda x: (x[1], x[0]))

            # Build angles list and dictionary by comparing each point to the first_point
            counter = 0
            for angle in circle_positions:
                if angle != first_point:

                    rise = angle[1] - first_point[1]
                    run = angle[0] - first_point[0]

                    if run == 0:
                        slopes.append(90)
                        slopes_dict[90] = counter

                    else:
                        slope = rise / run
                        slope = round(math.atan(slope) * 180/math.pi, 2)
                        if slope < 0:
                            slope = round(slope + 180, 2)

                        slopes.append(slope)
                        slopes_dict[slope] = counter

                elif angle == first_point:
                    slopes.append(0)
                    slopes_dict[0] = counter
                
                counter += 1
            
            # Sort angles
            slopes_sorted = sorted(slopes)

            # Sort points by ascending angle
            for i in slopes_sorted:
                index = slopes_dict[i]
                points_sorted_by_angle.append(circle_pos_dict[index])

            # Convex hull algorithm (Graham scan)
            for p in points_sorted_by_angle:
                while len(stack) > 1 and counterclockwise(stack[-2], stack[-1], p) <= 0:
                    stack = stack[:-1]
                    stack_draw = stack_draw[:-1]
                    lines = lines[:-1]
                stack.append(p)
                stack_draw.append(Circle())
                stack_draw[-1].circle_pos(p[0], p[1])
                stack_draw[-1].flip_y_coord()
                lines.append(Line())
            
            # ##################
            # For testing
            # ##################

            # print(circle_positions)
            # print(circle_pos_dict)
            # print(first_point)
            # print(slopes)
            # print(slopes_dict)
            # print(slopes_sorted)
            # print(points_sorted_by_angle)
            # print(stack)

            # Draw a single line if only two points
            if len(lines) == 2:
                lines[0].line_pos_start(stack[0][0], flip(stack[0][1]))
                lines[0].line_pos_end(stack[1][0], flip(stack[1][1]))

            # Connect and draw full convex hull (connect last point back to first point)
            if len(lines) > 2:
                for line in range(2, len(lines)):
                    lines[line-2].line_pos_start(stack[line-2][0], flip(stack[line-2][1]))
                    lines[line-2].line_pos_end(stack[line-1][0], flip(stack[line-1][1]))
                    lines[line-1].line_pos_start(stack[line-1][0], flip(stack[line-1][1]))
                    lines[line-1].line_pos_end(stack[line][0], flip(stack[line][1]))
                    lines[line].line_pos_start(stack[line][0], flip(stack[line][1]))
                    lines[line].line_pos_end(stack[0][0], flip(stack[0][1]))

            # Increment clicks
            clicks += 1

    # Displaying points and lines
    for count in range(len(circles)):
        circles[count].place_circle()
 
    for count in range(len(lines)):
        lines[count].place_line()
    
    pygame.display.update()
    clock.tick(60)
    