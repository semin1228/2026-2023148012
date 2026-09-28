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

def draw_character(x):
    clear_canvas()
    character.draw(x, 500)
    update_canvas()
    delay(0.01)
    

def move_right():
    print('RIGHT')
    pass

def move_bottom():
    print('BOTTOM')
    pass

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
