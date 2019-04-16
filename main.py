import enum
import time

import numpy as np
import pygame
from pygame.locals import QUIT


DELAY = 1 / 30


class Color(enum.Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
    PURPLE = 4
    YELLOW = 5


class Tetromino:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def step(self):
        self.height -= 1


class LShaped(Tetromino):
    pass


class JShaped(Tetromino):
    pass


class SShaped(Tetromino):
    pass


class ZShaped(Tetromino):
    pass


class IShaped(Tetromino):
    pass


class Square(Tetromino):
    pass


class Grid:
    def __init__(self, width, height):
        self.height = height
        self.width = width

        self.grid_height = 20
        self.grid_width = 10

        self.pixel_width = self.width // self.grid_width
        self.pixel_height = self.height // self.grid_height

    @staticmethod
    def draw_background(screen):
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        screen.blit(background, (0, 0))

    def draw(self, screen):
        pix_width = self.pixel_width
        pix_height = self.pixel_height
        for i in range(self.grid_width):
            for j in range(self.grid_height):
                rect = pygame.Rect(i * pix_width, j * pix_height, pix_width - 1, pix_height - 1)
                pygame.draw.rect(screen, (255, 255, 255), rect)


def main():
    pygame.display.init()
    screen = pygame.display.set_mode((300, 600))
    grid = Grid(300, 600, )
    pygame.display.set_caption("Tetris")

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        grid.draw_background(screen)
        grid.draw(screen)

        pygame.display.flip()
        time.sleep(DELAY)


main()


