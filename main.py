from stellar import StellarUnicorn
from picographics import PicoGraphics, DISPLAY_STELLAR_UNICORN
import time
import math

graphics = PicoGraphics(display=DISPLAY_STELLAR_UNICORN)
stellar_unicorn = StellarUnicorn()


BLACK = graphics.create_pen(0, 0, 0)
WHITE = graphics.create_pen(255, 255, 255)


class Player:
    def __init__(self, initial_x, up_button, down_button):
        self.height = 4
        self.y_top = 6
        self.x = initial_x
        self.up_button = up_button
        self.down_button = down_button

    def handle_button_press(self, stellar_unicorn):
        if stellar_unicorn.is_pressed(self.up_button):
            if self.y_top != 0:
                self.y_top -= 1
        elif stellar_unicorn.is_pressed(self.down_button):
            if self.y_top + self.height != StellarUnicorn.HEIGHT:
                self.y_top += 1

    def position(self):
        return (self.x, self.y_top, self.x, self.y_top + self.height)


class Ball:
    def __init__(self, initial_position, initial_direction, speed):
        self.x = initial_position[0]
        self.y = initial_position[1]
        self.x_direction = initial_direction[0]
        self.y_direction = initial_direction[1]
        self.speed = speed

    def update_position(self):
        normalisation_constant = self.speed / math.sqrt(
            self.x_direction ** 2 + self.y_direction ** 2
        )

        delta_x = round(normalisation_constant * self.x_direction)
        delta_y = round(normalisation_constant * self.y_direction)

        self.x += delta_x
        self.y += delta_y

    def position(self):
        return (self.x, self.y)


ball = Ball((int(StellarUnicorn.WIDTH / 2), int(StellarUnicorn.HEIGHT / 2)), (1, 1), 1)

players = [
    Player(0, StellarUnicorn.SWITCH_A, StellarUnicorn.SWITCH_B),
    Player(
        StellarUnicorn.WIDTH - 1,
        StellarUnicorn.SWITCH_VOLUME_UP,
        StellarUnicorn.SWITCH_VOLUME_DOWN,
    ),
]

while True:
    graphics.set_pen(BLACK)
    graphics.clear()

    # draw the text
    graphics.set_pen(WHITE)

    ball.update_position()
    graphics.rectangle(ball.x, ball.y, 1, 1)

    for player in players:
        player.handle_button_press(stellar_unicorn)
        graphics.line(*player.position())

    # update the display
    stellar_unicorn.update(graphics)

    time.sleep(0.2)
