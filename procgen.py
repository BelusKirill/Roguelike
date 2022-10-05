from __future__ import annotations #Что бы видить тип класса внутри самого класса

import random
import tcod
import tile_types

from typing import Iterator, Tuple, List, TYPE_CHECKING
from game_map import GameMap

if TYPE_CHECKING:
    from entity import Entity


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        return slice(self.x1 + 1, self.x2 - 1), slice(self.y1 + 1, self.y2 - 1)

    @property
    def wall(self) -> Tuple[slice, slice]:
        return slice(self.x1, self.x2), slice(self.y1, self.y2)

    def intersects(self, other: RectangularRoom) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )


# Генерация тунелей между комнатами (функция генераторо т.к return -> yield)
def tunnel_between(
    start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """Возращает L-образный туннель между этими двумя точками."""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:  # 50% шанс, т.к random() от 0 до 1.
        # Двигайтесь горизонтально потом вкриткально.
        corner_x, corner_y = x2, y1
    else:
        # # Двигайтесь вкриткально потом горизонтально.
        corner_x, corner_y = x1, y2

    # Сгенерируйте координаты для этого туннеля. 
    # yield - сохраняет локальные пораметры между вызовами и продолжить с того места, на котором она остановилась
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist(): # Функция для рисования линий Брезенхема
        yield x, y 
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    player: Entity,
    ) -> GameMap:
    """Generate a new dungeon map."""
    dungeon = GameMap(map_width, map_height)

    rooms: List[RectangularRoom] = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        new_room = RectangularRoom(x, y, room_width, room_height)

        # Проверка на пересечение комнат.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue

        # Создане комнаты
        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0: # Первоя комната
            player.x, player.y = new_room.center
        else:
            # Отрисовка тунеля от текущей и предыдущей.
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

        rooms.append(new_room)

    return dungeon