import math

import pygame
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])


class Player(pygame.sprite.Sprite):
    def __init__(self, starting_position: tuple):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.center = starting_position

    def update(self, pressed_keys: dict):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        elif pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def update(self, center_position: tuple):
        self.rect.move_ip(center_position)


class Ball(pygame.sprite.Sprite):
    def __init__(self, initial_direction: tuple, speed: int):
        super(Ball, self).__init__()
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.center = ((SCREEN_WIDTH-surf.get_width())/2,
                            (SCREEN_HEIGHT-surf.get_height())/2)
        self.direction = initial_direction
        self.speed = speed

    def update(self):
        normalisation_constant = (
            self.speed /
            math.sqrt(self.direction[0] ** 2 + self.direction[1] ** 2)
        )

        normalised_x = round(normalisation_constant * self.direction[0])
        normalised_y = round(normalisation_constant * self.direction[1])

        self.rect.move_ip(
            normalised_x,
            normalised_y
        )

    def get_position(self):
        return self.rect.center


clock = pygame.time.Clock()

surf = pygame.Surface((50, 50))
surf.fill((0, 0, 0))
rect = surf.get_rect()

surf_center_x = (SCREEN_WIDTH-surf.get_width())/2
surf_center_y = (SCREEN_HEIGHT-surf.get_height())/2
starting_y_offset = (SCREEN_HEIGHT*0.4)

player = Player((surf_center_x, surf_center_y + starting_y_offset))
computer = Player((surf_center_x, surf_center_y - starting_y_offset))
ball = Ball((1, 1), 1)

all_sprites = pygame.sprite.Group()
[all_sprites.add(p) for p in [player, computer, ball]]

bats = pygame.sprite.Group()
[bats.add(b) for b in [player, computer]]

balls = pygame.sprite.Group()
balls.add(ball)

screen.fill((0, 0, 0))

running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    # print(ball.get_position())
    computer.update(ball.get_position())

    ball.update()

    screen.fill((0, 0, 0))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(ball, bats):
        ball.direction = (ball.direction[0] * -1, ball.direction[1] * -1)

    pygame.display.flip()

    clock.tick(60)


pygame.quit()
