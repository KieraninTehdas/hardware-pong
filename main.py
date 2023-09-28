from stellar import StellarUnicorn
from picographics import PicoGraphics, DISPLAY_STELLAR_UNICORN
import time
import math
import random

graphics = PicoGraphics(display=DISPLAY_STELLAR_UNICORN)
stellar_unicorn = StellarUnicorn()
stellar_unicorn.set_brightness(0.5)


BLACK = graphics.create_pen(0, 0, 0)
WHITE = graphics.create_pen(255, 255, 255)


class PlayerControls:
    def __init__(self, up_button: str, down_button: str):
        self.up_button = up_button
        self.down_button = down_button


class Player:
    def __init__(self, initial_x, controls: PlayerControls):
        self.height = 4
        self.y_top = 6
        self.x = initial_x
        self.up_button = controls.up_button
        self.down_button = controls.down_button
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
    def __init__(self, spawn_box_ranges, speed):
        self.spawn_box_x_range = spawn_box_ranges[0]
        self.spawn_box_y_range = spawn_box_ranges[1]
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
        self.x = random.randint(*self.spawn_box_x_range)
        self.y = random.randint(*self.spawn_box_y_range)
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


class Game:
    def __init__(self, game_width, game_height, player_1_controls, player_2_controls):
        spawn_box_x_range = (6, game_width - 6)
        spawn_box_y_range = (6, game_height - 6)
        self.ball = Ball((spawn_box_x_range, spawn_box_y_range), 1)

        self.players = [
            Player(0, player_1_controls),
            Player(game_height - 1, player_2_controls),
        ]

        self.winner = None

    def find_colliding_player(self, ball, players):
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


class GameSurface:
    def __init__(self, stellar_unicorn: StellarUnicorn, graphics: PicoGraphics):
        self.stellar_unicorn = stellar_unicorn
        self.graphics = graphics

    def prepare(self):
        graphics.set_pen(BLACK)
        graphics.clear()
        graphics.set_pen(WHITE)

    def ball_sprite(self, ball):
        graphics.rectangle(ball.x, ball.y, 1, 1)

    def player_sprite(self, player):
        graphics.line(*player.position())

    def is_pressed_button(self, button):
        stellar_unicorn.is_pressed(button)


game = Game(
    StellarUnicorn.WIDTH,
    StellarUnicorn.HEIGHT,
    PlayerControls(StellarUnicorn.SWITCH_A, StellarUnicorn.SWITCH_B),
    PlayerControls(StellarUnicorn.SWITCH_VOLUME_UP, StellarUnicorn.SWITCH_VOLUME_DOWN),
)


while True:
    graphics.set_pen(BLACK)
    graphics.clear()

    graphics.set_pen(WHITE)

    game.ball.update_position()
    graphics.rectangle(game.ball.x, game.ball.y, 1, 1)

    for player in game.players:
        player.handle_button_press(stellar_unicorn)
        graphics.line(*player.position())

    colliding_player = game.find_colliding_player(game.ball, game.players)
    if colliding_player:
        game.ball.handle_collision(colliding_player.moving_direction)

    next_ball_y_position = game.ball.next_position()[1]

    if next_ball_y_position < 0 or next_ball_y_position > StellarUnicorn.HEIGHT - 1:
        game.ball.handle_edge_collision()

    next_ball_x_position = game.ball.next_position()[0]
    if next_ball_x_position < -1:
        game.ball.reset()
        time.sleep(1)
    elif next_ball_x_position > StellarUnicorn.WIDTH:
        game.ball.reset()
        time.sleep(1)

    # update the display
    stellar_unicorn.update(graphics)

    time.sleep(0.2)
