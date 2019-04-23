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
    CYAN = 3
    PURPLE = 4
    YELLOW = 5
    ORANGE = 6


class SingleBlock:
    def draw(self, screen):
        pass


class Tetromino:
    """
    Base class for all tetrominos.
    Each tetromino needs a color and coordinates.
    """

    color = ...
    coords = ...

    def __init__(self, i, j):
        self.i = i
        self.j = j

    def step(self):
        self.i += 1

    def rotate(self):
        self.coords = [(j, 3 - i) for i, j in self.coords]

    def draw(self, grid):
        pass


class LShaped(Tetromino):
    color = Color.BLUE
    coords = (
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 2)
    )


class JShaped(Tetromino):
    color = Color.ORANGE
    coords = (
        (1, 0),
        (1, 1),
        (1, 2),
        (0, 2)
    )


class SShaped(Tetromino):
    color = Color.GREEN
    coords = (
        (0, 0),
        (0, 1),
        (1, 1),
        (1, 2)
    )


class ZShaped(Tetromino):
    color = Color.RED
    coords = (
        (1, 0),
        (1, 1),
        (0, 1),
        (0, 2)
    )


class IShaped(Tetromino):
    color = Color.CYAN
    coords = (
        (0, 0),
        (0, 1),
        (0, 2),
        (0, 3)
    )


class Square(Tetromino):
    color = Color.YELLOW
    coords = (
        (0, 0),
        (1, 0),
        (0, 1),
        (1, 1)
    )


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

    def draw_grid(self, screen):
        pix_width = self.pixel_width
        pix_height = self.pixel_height
        for i in range(self.grid_width):
            for j in range(self.grid_height):
                rect = pygame.Rect(i * pix_width, j * pix_height, pix_width - 1, pix_height - 1)
                pygame.draw.rect(screen, (255, 255, 255), rect)

    def draw_tetrominos(self, screen):
        pass


def main():
    pygame.display.init()
    screen = pygame.display.set_mode((300, 600))
    grid = Grid(300, 600)
    pygame.display.set_caption("Tetris")

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        grid.draw_background(screen)
        grid.draw_grid(screen)

        pygame.display.flip()
        time.sleep(DELAY)


main()


