import logging
import random
import time
from itertools import product
from operator import attrgetter
from typing import Dict, List, Sequence, Tuple

import fire
import pygame
from pygame.locals import K_SPACE, QUIT

from .blocks import (
    GRID_HEIGHT,
    GRID_WIDTH,
    Color,
    IShaped,
    JShaped,
    LShaped,
    OShaped,
    SingleBlock,
    SShaped,
    TShaped,
    ZShaped,
    clear_lines,
)
from .network import run_server


logger = logging.getLogger(__name__)


GAME_NAME = "Snektris"
DELAY = 1 / 30
START_POSITION = (0, 4)


class Grid:
    def __init__(self, width, height, anchor_x=0, anchor_y=0):
        self.width = width
        self.height = height

        self.anchor_x = anchor_x
        self.anchor_y = anchor_y

        self.grid_height = GRID_HEIGHT
        self.grid_width = GRID_WIDTH

        self.pixel_width = self.width // self.grid_width
        self.pixel_height = self.height // self.grid_height

    def draw_background(self, screen):
        background = pygame.Surface((self.width, self.height))
        background = background.convert()
        background.fill(Color.LINE_COLOR.value)
        screen.blit(background, (self.anchor_x, self.anchor_y))

    def draw_grid(self, screen):
        pix_width = self.pixel_width
        pix_height = self.pixel_height
        for i, j in product(range(self.grid_height), range(self.grid_width)):
            rect = pygame.Rect(
                j * pix_width + self.anchor_x,
                i * pix_height + self.anchor_y,
                pix_width - 1,
                pix_height - 1,
            )
            pygame.draw.rect(screen, Color.BACKGROUND.value, rect)

    def draw_snektrominos(self, screen, blocks, active_snektromino):
        pix_width = self.pixel_width
        pix_height = self.pixel_height
        for block in [*active_snektromino.blocks, *blocks.values()]:
            i, j = block.coords
            color = block.color
            rect = pygame.Rect(
                j * pix_width + self.anchor_x,
                i * pix_height + self.anchor_y,
                pix_width - 1,
                pix_height - 1,
            )
            pygame.draw.rect(screen, color.value, rect)


def update_blocks(blocks, new_blocks):
    for block in new_blocks:
        blocks[block.coords] = block


def process_input(event, active_snektromino, blocks):
    new_snektromino = None

    if event.type == pygame.KEYDOWN:

        if event.key == pygame.K_x:
            new_snektromino = active_snektromino.rotate_clockwise()

        elif event.key == pygame.K_y:
            new_snektromino = active_snektromino.rotate_anticlockwise()

        if event.key == pygame.K_LEFT:
            new_snektromino = active_snektromino.step_left()

        if event.key == pygame.K_RIGHT:
            new_snektromino = active_snektromino.step_right()

        if event.key == pygame.K_DOWN:
            new_snektromino = active_snektromino.step_down()

        if event.key == pygame.K_UP:
            new_snektromino = active_snektromino.fall_down(blocks)
    return new_snektromino


def run_game():
    counter = 0
    game_over = False

    blocks = {}

    while not game_over:

        snektromino_class = random.choice(
            [SShaped, TShaped, ZShaped, LShaped, IShaped, JShaped, OShaped]
        )
        active_snektromino = snektromino_class(*START_POSITION)

        while True:
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():

                if event.type == QUIT:
                    return

                new_snektromino = process_input(event, active_snektromino, blocks)

            if (
                new_snektromino
                and new_snektromino.within_boundaries()
                and not new_snektromino.overlaps_with(blocks)
            ):
                active_snektromino = new_snektromino

            if counter == 30:
                new_snektromino = active_snektromino.step_down()
                if new_snektromino.within_boundaries() and not new_snektromino.overlaps_with(
                    blocks
                ):
                    active_snektromino = new_snektromino
                else:
                    active_snektromino.done = True

                counter = 0

            counter += 1

            if active_snektromino.done:
                update_blocks(blocks, active_snektromino.blocks)

                if START_POSITION in blocks:
                    game_over = True
                break

            blocks = clear_lines(blocks)

            yield blocks, active_snektromino


def single(seed=None, debug=False):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    random.seed(seed)
    pygame.display.init()
    screen = pygame.display.set_mode((300, 600))
    grid = Grid(300, 600)
    pygame.display.set_caption(GAME_NAME)

    for blocks, active_snektromino in run_game():
        grid.draw_background(screen)
        grid.draw_grid(screen)
        grid.draw_snektrominos(screen, blocks, active_snektromino)
        pygame.display.flip()
        time.sleep(DELAY)


def multi(mode, host="localhost", port=8080, *, seed=None, debug=False):
    mode = mode.lower()
    if mode not in ("client", "server"):
        raise ValueError("Choose between 'client' and 'server'")

    if debug:
        logging.basicConfig(level=logging.DEBUG)
    random.seed(seed)
    pygame.display.init()
    screen = pygame.display.set_mode((800, 600))
    grid = Grid(300, 600)
    grid2 = Grid(300, 600, 500, 0)
    pygame.display.set_caption(GAME_NAME)

    with run_server(host, port) as q:
        for blocks, active_snektromino in run_game():
            grid.draw_background(screen)
            grid.draw_grid(screen)
            grid.draw_snektrominos(screen, blocks, active_snektromino)
            if not q.empty():
                logger.debug("Found something in queue")
                remote_blocks = q.get()
                grid2.draw_background(screen)
                grid2.draw_grid(screen)
                grid2.draw_snektrominos(screen, remote_blocks, active_snektromino)
            pygame.display.flip()
            time.sleep(DELAY)


def cli():
    fire.Fire({"single": single, "multi": multi})
