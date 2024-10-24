from enum import Enum


class CellState(Enum):
    HIT = "x"
    MISS = "o"
    EMPTY = "."
    SHIP = "s"
    UNKNOWN = "?"
