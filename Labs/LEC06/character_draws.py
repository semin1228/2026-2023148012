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
        draw_character(x, y)


def move_top():
    print('TOP')
    for x in range(50, 750, 5):
        draw_character(x, 550)

def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(0.01)


def move_right():
    print('RIGHT')
    for y in range(550, 50, -5):
        draw_character(750, y)

def move_bottom():
    print('BOTTOM')
    for x in range(750, 50, -5):
        draw_character(x, 50)

def move_left():
    print('LEFT')
    pass

def draw_rectangle():
    print('RECTANGLE')
    move_top()
    move_right()
    move_bottom()
    move_left()
    pass


def draw_triangle():
    print('TRIANGLE')

while True:
    draw_circle()
    draw_rectangle()
    draw_triangle()
    break

delay(1)
close_canvas()
