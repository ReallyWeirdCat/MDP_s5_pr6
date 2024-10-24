import random

from config import BOARD_SIZE
from exceptions import PointOutOfBoundsError


class Position:

    x = 0
    y = 0

    def __init__(self, x: int, y: int):

        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError("Координаты должны быть целыми числами")

        for coordinate in (x, y):

            if coordinate < 0 or coordinate > BOARD_SIZE:
                raise PointOutOfBoundsError("Координата за пределами поля")

        self.x = x
        self.y = y

    # Random Position
    @staticmethod
    def random():
        return Position(random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1))
