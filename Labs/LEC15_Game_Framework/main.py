from pico2d import *
import logo_mode

open_canvas()
logo_mode.init()
# game loop
while logo_mode.running:
    logo_mode.handle_events()
    logo_mode.update()
    logo_mode.render()
    delay(0.01)
logo_mode.finish()
close_canvas()