<p align="center">
  <img src="https://www.mirea.ru/upload/medialibrary/c1a/MIREA_Gerb_Colour.jpg" alt="MIREA" width="80"/>
  <img src="https://www.mirea.ru/upload/medialibrary/26c/FTI_colour.jpg" alt="IPTIP" width="137"/> 
</p>

# Математика для программирования (часть 1/2) [I.24-25]

## Практическое занятие 6. Морской бой.
Работу выполнил студент `Папин Николай Алексеевич` группы `ЭФБО-02-22` с вариантом `5.2`.

## Описание проекта
Реализована игра `Морской бой` на поле с размерностью `6х6` и с двумя кораблями длиной `2`.

### Функции
- [x] Размещение корабля
    - [x] Проверка координат
    - [x] Проверка пересечений
    - [x] Проверка умещения
    - [x] Случайное расположение для ИИ
- [x] Отображение поля игрока
- [x] Отображение поля противника с туманом войны
- [x] Проверки на попадание
- [x] Иллюзорный ИИ противника
- [x] Определение победы

### Ответы на вопросы

#### Как создается массив и как в него записываются объекты.
Для хранения игровых полей используется объект `Board`. Он содержит в себе аттрибуты `matrix` и `fog_matrix`, которые представляют собой двумерные массивы клеток. При инициализации объекта `Board` массивы заполняются при помощи генераторов списков:
```python
        self.matrix = [[CellState.EMPTY for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
        self.fog_matrix = [[CellState.UNKNOWN for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
```
Для хранения вида клетки используется объект `cellState`, унаследованный от `enum.Enum`:
```python
from enum import Enum

class CellState(Enum):
    HIT = "x"
    MISS = "o"
    EMPTY = "."
    SHIP = "s"
    UNKNOWN = "?"
```
Для расположения кораблей в классе `Board` реализован метод `placeShip`. Учитывая максимальное допустимое количество кораблей, пересечения и размеры карты, он позволяет выполнять расположения кораблей и совершает валидацию позиций. В случае, если все условия верны, заполнение клеток корабля происходит следующим образом:
```python
for i in range(SHIP_SIZE):
            if dir == Direction.NORTH:
                self.matrix[pos.y - i][pos.x] = CellState.SHIP
            if dir == Direction.SOUTH:
                self.matrix[pos.y + i][pos.x] = CellState.SHIP
            if dir == Direction.EAST:
                self.matrix[pos.y][pos.x + i] = CellState.SHIP
            if dir == Direction.WEST:
                self.matrix[pos.y][pos.x - i] = CellState.SHIP
```

#### Как происходит взаимодействие при выстрелах.
При выстреле с помощью метода `attackCell`, точка в матрице меняет свое значения на `cellState.HIT` или `cellState.MISS` в зависимости от того, был ли в ней расположен корабль.
#### Как изменяется массив в процессе игры
При помощи функции `attackCell`, на каждом шаге терпят изменения либо поле игрока, либо поле ИИ. Каждая доска `Board` имеет массивы `matrix` и `fog_matrix`, где последний используется для отображения поля с туманом войны (его видит противник). 
```python
 def attackCell(self, position):

        if self.matrix[position.y][position.x] == CellState.SHIP:
            self.matrix[position.y][position.x] = CellState.HIT
            self.fog_matrix[position.y][position.x] = CellState.HIT
            self.ship_cells -= 1
            return True

        self.matrix[position.y][position.x] = CellState.MISS
        self.fog_matrix[position.y][position.x] = CellState.MISS
        return False
```

