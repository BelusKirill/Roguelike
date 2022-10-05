from typing import Tuple

import numpy as np  # type: ignore

# Плиточный графический структурированный тип, совместимый с Console.tiles_rgb.
graphic_dt = np.dtype(
    [
        ("ch", np.int32),  # Unicode codepoint.
        ("fg", "3B"),  # 3 байта без знака для цветов RGB. /Цвет символа
        ("bg", "3B"),  # Цвет фона
    ]
)

# Структура плитки, используемая для статически определенных данных плитки.
tile_dt = np.dtype(
    [
        ("walkable", np.bool),  # True если по этой плитке можно пройти.
        ("transparent", np.bool),  # True если эта плитка не блокирует FOV.
        ("dark", graphic_dt),  # Графика для случаев, когда эта плитка не находится в поле зрения.
    ]
)


def new_tile(
    *,  # Принудительно используйте ключевые слова, чтобы порядок параметров не имел значения.
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array((walkable, transparent, dark), dtype=tile_dt)


floor = new_tile(
    walkable=True, transparent=True, dark=(ord(" "), (255, 255, 255), (79, 102, 65)),
)
wall = new_tile(
    walkable=False, transparent=False, dark=(ord(" "), (255, 255, 255), (70, 70, 90)),
)