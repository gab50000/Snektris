import time

import numpy as np
import pygame
from pygame.locals import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((300, 600))
    pygame.display.set_caption("Tetris")

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    while True:
        random = np.random.randint(255, size=(300, 600, 3))
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        surf = pygame.surfarray.make_surface(random)
        screen.blit(surf, (0, 0))
        pygame.display.flip()


main()


