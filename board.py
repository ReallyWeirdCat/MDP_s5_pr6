import random

from config import BOARD_SIZE, SHIP_SIZE, SHIP_AMOUNT, HIT_CHANCE
from position import Position
from direction import Direction
from cellState import CellState
from exceptions import ShipOutOfBoundsError, ShipCollisionError, ShipLimitError, PointAlreadyHitError


class Board:

    matrix = None
    fog_matrix = None
    ship_cells = 0
    ships_placed = 0

    def __init__(self):
        self.matrix = [[CellState.EMPTY for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
        self.fog_matrix = [[CellState.UNKNOWN for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]

    def placeShip(self, pos: Position, dir: Direction):

        # Проверка количества кораблей
        if self.ships_placed == SHIP_AMOUNT:
            raise ShipLimitError

        # Проверка на выход за пределы карты
        if dir == Direction.NORTH and pos.y - SHIP_SIZE + 1 < 0:
            raise ShipOutOfBoundsError
        if dir == Direction.SOUTH and pos.y + SHIP_SIZE - 1 >= BOARD_SIZE:
            raise ShipOutOfBoundsError
        if dir == Direction.EAST and pos.x + SHIP_SIZE - 1 >= BOARD_SIZE:
            raise ShipOutOfBoundsError
        if dir == Direction.WEST and pos.x - SHIP_SIZE - 1 < 0:
            raise ShipOutOfBoundsError

        # Проверка на пересечение
        for i in range(SHIP_SIZE-1):
            if dir == Direction.NORTH:
                if self.matrix[pos.y - i][pos.x] == CellState.SHIP:
                    raise ShipCollisionError
            if dir == Direction.SOUTH:
                if self.matrix[pos.y + i - 1][pos.x] == CellState.SHIP:
                    raise ShipCollisionError
            if dir == Direction.EAST:
                if self.matrix[pos.y][pos.x + i - 1] == CellState.SHIP:
                    raise ShipCollisionError
            if dir == Direction.WEST:
                if self.matrix[pos.y][pos.x - i] == CellState.SHIP:
                    raise ShipCollisionError

        # Установка клеток корабля
        for i in range(SHIP_SIZE):
            if dir == Direction.NORTH:
                self.matrix[pos.y - i][pos.x] = CellState.SHIP
            if dir == Direction.SOUTH:
                self.matrix[pos.y + i][pos.x] = CellState.SHIP
            if dir == Direction.EAST:
                self.matrix[pos.y][pos.x + i] = CellState.SHIP
            if dir == Direction.WEST:
                self.matrix[pos.y][pos.x - i] = CellState.SHIP

        self.ships_placed += 1
        self.ship_cells += SHIP_SIZE

    def randomizeShips(self):
        while self.ships_placed < SHIP_AMOUNT:
            try:
                pos = Position.random()
                dir = Direction(random.randint(0, 3))

                self.placeShip(pos, dir)
            except Exception:
                continue

    def getCellStatus(self, position):
        return self.matrix[position.y][position.x]

    def attackCell(self, position):

        if self.matrix[position.y][position.x] == CellState.SHIP:
            self.matrix[position.y][position.x] = CellState.HIT
            self.fog_matrix[position.y][position.x] = CellState.HIT
            self.ship_cells -= 1
            return True

        self.matrix[position.y][position.x] = CellState.MISS
        self.fog_matrix[position.y][position.x] = CellState.MISS
        return False

    def randomAttack(self):

        position = None
        while not position:
            if random.random() < HIT_CHANCE:
                occupied = []
                for i in range(BOARD_SIZE):
                    for j in range(BOARD_SIZE):
                        if self.getCellStatus(Position(i, j)) == CellState.SHIP:
                            occupied.append(Position(i, j))

                if occupied:
                    position = random.choice(occupied)

            else:
                while True:
                    position = Position.random()
                    if self.getCellStatus(position) not in (CellState.HIT, CellState.MISS):
                        break
                    else:
                        position = None

        return self.attackCell(position)

    def isDead(self):
        if self.ship_cells <= 0:
            return True
        else:
            return False

    def printBoard(self):
        print("  0 1 2 3 4 5 ")
        for idx, i in enumerate(range(BOARD_SIZE)):
            print(str(i) + " ", end="")
            for j in range(BOARD_SIZE):

                if self.matrix[i][j] == CellState.EMPTY:
                    print(".", end=" ")
                elif self.matrix[i][j] == CellState.MISS:
                    print("o", end=" ")
                elif self.matrix[i][j] == CellState.HIT:
                    print("X", end=" ")
                elif self.matrix[i][j] == CellState.SHIP:
                    print("S", end=" ")
            print()
        print("-"*BOARD_SIZE)

    def printFogBoard(self):
        print("  0 1 2 3 4 5")
        for idx, i in enumerate(range(BOARD_SIZE)):
            print(str(i) + " ", end="")
            for j in range(BOARD_SIZE):

                if self.fog_matrix[i][j] == CellState.UNKNOWN:
                    print(".", end=" ")
                elif self.fog_matrix[i][j] == CellState.MISS:
                    print("o", end=" ")
                elif self.fog_matrix[i][j] == CellState.HIT:
                    print("X", end=" ")
                elif self.fog_matrix[i][j] == CellState.SHIP:
                    print("S", end=" ")
            print("")
        print("-"*BOARD_SIZE)
