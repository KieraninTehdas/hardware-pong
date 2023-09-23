from stellar import StellarUnicorn
from picographics import PicoGraphics, DISPLAY_STELLAR_UNICORN
import time

# create a PicoGraphics framebuffer to draw into
graphics = PicoGraphics(display=DISPLAY_STELLAR_UNICORN)

# create our StellarUnicorn object
stellar_unicorn = StellarUnicorn()

# start position for scrolling (off the side of the display)
scroll = float(-StellarUnicorn.WIDTH)


# pen colours to draw with
BLACK = graphics.create_pen(0, 0, 0)
WHITE = graphics.create_pen(255, 255, 255)

while True:
    # clear the graphics object
    graphics.set_pen(BLACK)
    graphics.clear()

    # draw the text
    graphics.set_pen(WHITE)

    graphics.line(0, 6, 0, 9)
    graphics.line(StellarUnicorn.WIDTH - 1, 6, StellarUnicorn.WIDTH - 1, 9)

    # update the display
    stellar_unicorn.update(graphics)

