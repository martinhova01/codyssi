from itertools import product


def directions4() -> list[tuple[int, int]]:
    return [(0,1),(1,0),(0,-1),(-1,0)]

def directions8() -> list[tuple[int, int]]:
    return [(dx, dy) for dx, dy in product((-1,0,1), repeat=2) if not dx == dy == 0]

def adjacent4(x: int, y: int) -> list[tuple[int, int]]:
    return [(x + dx, y + dy) for dx, dy in directions4()]

def adjacent8(x: int, y: int) -> list[tuple[int, int]]:
    return [(x + dx, y + dy) for dx, dy in directions8()]

def manhattanDist(x1, y1, x2, y2) -> int|float:
    return abs(x1 - x2) + abs(y1 - y2)

def rot90(x, y, clock_wise = True) -> tuple[int, int]:
    return (-y, x) if clock_wise else (y, -x)