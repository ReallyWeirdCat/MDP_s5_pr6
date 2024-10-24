from position import Position
from direction import Direction
from board import Board
from config import SHIP_AMOUNT
from exceptions import PointOutOfBoundsError, ShipOutOfBoundsError, PointAlreadyHitError


class Game:

    field_player = None
    field_computer = None
    turn = None

    def __init__(self):
        self.field_player = Board()
        self.field_computer = Board()
        self.turn = 0

    def think(self):

        while self.field_player.ships_placed < SHIP_AMOUNT:

            try:
                print("Капитан, разместите лодку!")
                pos = Position(int(input("x: ")), int(input("y: ")))
                print("Так точно! Необходимо выбрать направление!")
                dir = Direction(int(input("(Св: 1; Вс: 2; Юг: 3; Зп: 4): ")))

                self.field_player.placeShip(pos, dir)
            except PointOutOfBoundsError:
                print("Никак нет, Капитан, - точка расположена в нейтральных водах!")
                continue
            except ShipOutOfBoundsError:
                print("Никак нет, Капитан, - лодка выходит за пределы карты!")
                continue

        print("Капитан, ваши лодки готовы! Вражеский флот размещает посудину...")
        self.field_computer.randomizeShips()
        print("Вражеская посудина прибыла, Капитан!")

        while not self.field_computer.isDead() + self.field_player.isDead():

            if self.turn == 0:
                try:
                    print("Капитан, мы готовы атаковать позиции врага!")
                    pos = Position(int(input("x: ")), int(input("y: ")))

                    hit = self.field_computer.attackCell(pos)

                    if hit:
                        print("Попадание!")
                        continue

                    print("Точка оказалась пуста, Капитан!")

                except PointOutOfBoundsError:
                    print("Цель вне зоны поражения, Капитан!")
                    continue
                except PointAlreadyHitError:
                    print("Никак нет, Капитан! Мы уже стреляли в эту точку!")
                    continue

            else:
                print("Противник атакует!")

                hit = self.field_player.randomAttack()

                if hit:
                    print("Нас подбили!")
                    continue

                print("Противник промахнулся!")

            self.turn = (self.turn + 1) % 2

        if self.field_computer.isDead():
            print("Капитан, мы одержали победу!")
        else:
            print("Капитан, наш флот потерпел поражение!")
