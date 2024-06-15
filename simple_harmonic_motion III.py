import pygame
import random
import math
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1200,800))
pygame.display.set_caption('Simple Harmonic Motion III')
clock = pygame.time.Clock()

class Oscillator():

    def __init__(self):
        pass

w = screen.get_width() + 16
y_spacing = 10
max_waves = 5

theta = 0
amplitude = []
dx = []
xvalues = []

for i in range(max_waves):
    amplitude.append(random.randint(10,30))
    period = random.randint(100,300)
    dx.append((math.pi / period) * y_spacing)

def calc_wave(theta=0, xvalues=[], y_spacing=10, amplitude=[], dx=[], w=screen.get_width()+16):

    theta += 0.01
    for i in range(math.floor(w / y_spacing)):
        xvalues.append(0)
    
    for i in range(max_waves):
        x = theta
        for j in range(len(xvalues)):
            if (i%2==0):
                xvalues[j] += math.sin(x) * amplitude[i]
            else:
                xvalues[j] += math.cos(x) * amplitude[i]
            x += dx[i]

def render_wave():

    for i in range(len(xvalues)):
        pygame.draw.circle(screen,'white', (i*y_spacing, screen.get_width()/2 + xvalues[i], 30))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill('black')

    calc_wave()
    render_wave()

    pygame.display.update()
    clock.tick(60)