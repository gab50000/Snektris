import time

import numpy as np
import pygame
from pygame.locals import QUIT


DELAY = 1 / 30

LINE_COLOR = (200, 200, 200)
BACKGROUND = (50, 50, 50)
RED = (256, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)


class SingleBlock:
    def __init__(self, i, j, color):
        self.i = i
        self.j = j
        self.color = color

    @property
    def coords(self):
        return self.i, self.j

    @coords.setter
    def coords(self, new_coords):
        self.i, self.j = new_coords

    def step_down(self):
        self.i += 1

    def step_left(self):
        self.j -= 1

    def step_right(self):
        self.j += 1



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
        self.blocks = [SingleBlock(self.i + i, self.j + j, self.color)
                       for i, j in self.coords]

    def step_down(self):
        for block in self.blocks:
            block.step_down()

    def step_left(self):
        for block in self.blocks:
            block.step_left()

    def step_right(self):
        for block in self.blocks:
            block.step_right()

    def rotate(self):
        for block in self.blocks:
            block.coords = block.j, 3 - block.i


class LShaped(Tetromino):
    color = BLUE
    coords = (
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 2)
    )


class JShaped(Tetromino):
    color = ORANGE
    coords = (
        (1, 0),
        (1, 1),
        (1, 2),
        (0, 2)
    )


class SShaped(Tetromino):
    color = GREEN
    coords = (
        (0, 0),
        (0, 1),
        (1, 1),
        (1, 2)
    )


class TShaped(Tetromino):
    color = PURPLE
    coords = (
        (0, 1),
        (1, 0),
        (1, 1),
        (2, 1)
    )


class ZShaped(Tetromino):
    color = RED
    coords = (
        (1, 0),
        (1, 1),
        (0, 1),
        (0, 2)
    )


class IShaped(Tetromino):
    color = CYAN
    coords = (
        (0, 0),
        (0, 1),
        (0, 2),
        (0, 3)
    )


class Square(Tetromino):
    color = YELLOW
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

        self.blocks = []

    @staticmethod
    def draw_background(screen):
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill(LINE_COLOR)
        screen.blit(background, (0, 0))

    def draw_grid(self, screen):
        pix_width = self.pixel_width
        pix_height = self.pixel_height
        for i in range(self.grid_width):
            for j in range(self.grid_height):
                rect = pygame.Rect(i * pix_width, j * pix_height, pix_width - 1, pix_height - 1)
                pygame.draw.rect(screen, BACKGROUND, rect)

        for block in self.blocks:
            i, j = block.coordinates
            color = block.color

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


if __name__ == "__main__":
    main()


