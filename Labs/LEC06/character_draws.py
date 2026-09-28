from pico2d import *
import math

open_canvas(800, 600)
character = load_image('character.png')



def draw_circle():
    print('CIRCLE')

    for degree in range(360):
        theta = math.radians(degree)
        x = 400 + 200 * math.cos(theta)
        y = 300 + 200 * math.sin(theta)
        clear_canvas()
        character.draw(x, y)
        update_canvas()
        delay(0.05)


def draw_rectangle():
    print('RECTANGLE')


def draw_triangle():
    print('TRIANGLE')

while True:
    draw_circle()
    draw_rectangle()
    draw_triangle()
    break

delay(1)
close_canvas()
