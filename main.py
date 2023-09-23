from stellar import StellarUnicorn
from picographics import PicoGraphics, DISPLAY_STELLAR_UNICORN
import time
import math
import random

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
        self.moving_direction = 0

    def handle_button_press(self, stellar_unicorn):
        if stellar_unicorn.is_pressed(self.up_button):
            if self.y_top != 0:
                self.y_top -= 1
                self.moving_direction = -1
        elif stellar_unicorn.is_pressed(self.down_button):
            if self.y_top + self.height != StellarUnicorn.HEIGHT:
                self.y_top += 1
                self.moving_direction = 1
        else:
            self.moving_direction = 0

    def position(self):
        return (self.x, self.y_top, self.x, self.y_top + self.height)


class Ball:
    def __init__(self, initial_position, speed):
        self.initial_position = initial_position
        self.speed = speed
        self.reset()

    def reset_direction(self):
        if random.random() >= 0.5:
            self.x_direction = 1
        else:
            self.x_direction = -1

        y_random = random.random()

        if y_random > 0.55:
            self.y_direction = 1
        elif y_random < 45:
            self.y_direction = -1
        else:
            self.y_direction = 0

    def reset(self):
        self.x = self.initial_position[0]
        self.y = self.initial_position[1]
        self.reset_direction()

    def next_position(self):
        normalisation_constant = self.speed / math.sqrt(
            self.x_direction ** 2 + self.y_direction ** 2
        )

        delta_x = round(normalisation_constant * self.x_direction)
        delta_y = round(normalisation_constant * self.y_direction)

        return (self.x + delta_x, self.y + delta_y)

    def update_position(self):
        next_position = self.next_position()
        self.x = next_position[0]
        self.y = next_position[1]

    def handle_collision(self, y_momentum_direction):
        self.x_direction = -self.x_direction
        if self.y_direction == 0:
            self.y_direction = y_momentum_direction

    def handle_edge_collision(self):
        self.y_direction = -self.y_direction

    def position(self):
        return (self.x, self.y)


def find_colliding_player(ball, players):
    next_ball_position = ball.next_position()

    maybe_colliding_player = None

    if next_ball_position[0] == 0:
        maybe_colliding_player = players[0]

    if next_ball_position[0] == StellarUnicorn.WIDTH - 1:
        maybe_colliding_player = players[1]

    if maybe_colliding_player is None:
        return

    if (
        maybe_colliding_player.y_top
        <= next_ball_position[1]
        <= maybe_colliding_player.y_top + maybe_colliding_player.height
    ):
        return maybe_colliding_player


ball = Ball((int(StellarUnicorn.WIDTH / 2), int(StellarUnicorn.HEIGHT / 2)), 1)

players = [
    Player(0, StellarUnicorn.SWITCH_A, StellarUnicorn.SWITCH_B),
    Player(
        StellarUnicorn.WIDTH - 1,
        StellarUnicorn.SWITCH_VOLUME_UP,
        StellarUnicorn.SWITCH_VOLUME_DOWN,
    ),
]

winner = None

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

    colliding_player = find_colliding_player(ball, players)
    if colliding_player:
        ball.handle_collision(colliding_player.moving_direction)

    next_ball_y_position = ball.next_position()[1]

    if next_ball_y_position < 0 or next_ball_y_position > StellarUnicorn.HEIGHT - 1:
        ball.handle_edge_collision()

    next_ball_x_position = ball.next_position()[0]
    if next_ball_x_position < 0:
        ball.reset()
        winner = "Player 2"
    elif next_ball_x_position > StellarUnicorn.WIDTH - 1:
        winner = "Player 1"
        ball.reset()

    # update the display
    stellar_unicorn.update(graphics)

    time.sleep(0.2)
