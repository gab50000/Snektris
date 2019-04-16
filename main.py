import time

import numpy as np
import pygame
from pygame.locals import *


class Tetris:
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


def main():
    pygame.display.init()
    screen = pygame.display.set_mode((300, 600))
    tetris = Tetris(300, 600, )
    pygame.display.set_caption("Tetris")

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        tetris.draw_background(screen)
        tetris.draw_grid(screen)

        pygame.display.flip()
        time.sleep(1/30)


main()


