import logging
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Sequence, Tuple

logger = logging.getLogger(__name__)


GRID_HEIGHT = 20
GRID_WIDTH = 10


class Color(Enum):
    LINE_COLOR = (200, 200, 200)
    BACKGROUND = (50, 50, 50)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    CYAN = (0, 255, 255)
    PURPLE = (128, 0, 128)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 165, 0)


@dataclass
class SingleBlock:
    i: int
    j: int
    color: Color

    def __repr__(self):
        return f"SingleBlock({self.i}, {self.j}, {self.color})"

    @property
    def coords(self):
        return self.i, self.j

    @coords.setter
    def coords(self, new_coords):
        self.i, self.j = new_coords

    def step_down(self):
        return SingleBlock(self.i + 1, self.j, self.color)

    def step_left(self):
        return SingleBlock(self.i, self.j - 1, self.color)

    def step_right(self):
        return SingleBlock(self.i, self.j + 1, self.color)

    def rotate_clockwise(self, i, j):
        ii = self.i - i
        jj = self.j - j
        return SingleBlock(i + jj, j - ii, self.color)

    def rotate_anticlockwise(self, i, j):
        ii = self.i - i
        jj = self.j - j
        return SingleBlock(i - jj, j + ii, self.color)


class Snektromino:
    """
    Base class for all snektrominos.
    Each snektromino needs a color and coordinates.
    """

    color: Color
    initial_coords: Sequence[Tuple[int, int]]

    def __init__(self, i, j, blocks=None):
        self.i = i
        self.j = j
        if blocks:
            self.blocks = blocks
        else:
            self.blocks = [
                SingleBlock(self.i + i, self.j + j, self.color)
                for i, j in self.initial_coords
            ]
        self.done = False

    def __repr__(self):
        return self.blocks.__repr__()

    def step_down(self):
        new_blocks = [block.step_down() for block in self.blocks]
        return type(self)(self.i + 1, self.j, new_blocks)

    def fall_down(self, other_positions):
        new_piece = self.step_down()

        if new_piece.within_boundaries() and not new_piece.overlaps_with(
            other_positions
        ):
            return new_piece.fall_down(other_positions)
        self.done = True
        return self

    def step_left(self):
        new_blocks = [block.step_left() for block in self.blocks]
        return type(self)(self.i, self.j - 1, new_blocks)

    def step_right(self):
        new_blocks = [block.step_right() for block in self.blocks]
        return type(self)(self.i, self.j + 1, new_blocks)

    def rotate_clockwise(self):
        logger.debug("Before rotation: %s", self)
        new_blocks = [block.rotate_clockwise(self.i, self.j) for block in self.blocks]
        return type(self)(self.i, self.j, new_blocks)

    def rotate_anticlockwise(self):
        logger.debug("Before rotation: %s", self)
        new_blocks = [
            block.rotate_anticlockwise(self.i, self.j) for block in self.blocks
        ]
        return type(self)(self.i, self.j, new_blocks)

    def within_boundaries(self):
        for block in self.blocks:
            if block.j < 0:
                return False

            if block.j > GRID_WIDTH - 1:
                return False

            if block.i > GRID_HEIGHT - 1:
                return False
        return True

    def overlaps_with(self, other_blocks: Dict[Tuple[int, int], SingleBlock]):
        return any(block.coords in other_blocks for block in self.blocks)


# fmt: off
class LShaped(Snektromino):
    color = Color.BLUE
    initial_coords = (
        (-1, 0),
        ( 0, 0),
        ( 1, 0),
        ( 1, 1)
    )


class JShaped(Snektromino):
    color = Color.ORANGE
    initial_coords = (
        (-1,  0),
        ( 0,  0),
        ( 1,  0),
        ( 1, -1)
    )


class SShaped(Snektromino):
    color = Color.GREEN
    initial_coords = (
        (-1, 0),
        ( 0, 0),
        ( 0, 1),
        ( 1, 1)
    )


class TShaped(Snektromino):
    color = Color.PURPLE
    initial_coords = (
        (-1,  0),
        ( 0, -1),
        ( 0,  0),
        ( 1,  0)
    )


class ZShaped(Snektromino):
    color = Color.RED
    initial_coords = (
        (-1,  0),
        ( 0,  0),
        ( 0, -1),
        ( 1, -1)
    )


class IShaped(Snektromino):
    color = Color.CYAN
    initial_coords = (
        (-1, 0),
        ( 0, 0),
        ( 1, 0),
        ( 2, 0)
    )


class OShaped(Snektromino):
    color = Color.YELLOW
    initial_coords = (
        (0, 0),
        (1, 0),
        (0, 1),
        (1, 1)
    )

    def rotate_clockwise(self):
        return self

    def rotate_anticlockwise(self):
        return self

# fmt: on


def clear_lines(
    blocks: Dict[Tuple[int, int], SingleBlock]
) -> Dict[Tuple[int, int], SingleBlock]:

    lines_to_be_deleted = []
    steps_to_take = [0] * GRID_HEIGHT
    new_blocks = {}

    steps = 0
    for i in reversed(range(GRID_HEIGHT)):
        steps_to_take[i] = steps
        if all((i, j) in blocks for j in range(GRID_WIDTH)):
            lines_to_be_deleted.append(i)
            steps += 1

    if lines_to_be_deleted:

        for (ii, jj), block in blocks.items():
            if ii in lines_to_be_deleted:
                continue

            new_block = block
            steps = steps_to_take[ii]
            for _ in range(steps):
                new_block = new_block.step_down()
            new_blocks[(ii + steps, jj)] = new_block

        blocks = new_blocks
    return blocks


def blocks_from_list(list_):
    blocks = {}
    for i, line in enumerate(list_):
        for j, val in enumerate(line):
            if val:
                blocks[(i, j)] = SingleBlock(i, j, None)
    return blocks


def blocks_to_list(blocks):
    list_ = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for i, j in blocks:
        list_[i][j] = 1
    return list_
