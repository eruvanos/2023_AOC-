import math
from typing import NamedTuple, Iterable, Tuple


def neigbors(vec: "Vec2"):
    """Manhattan neighbors inc diagonal, clockwise"""
    vec = Vec2(*vec)
    yield vec + (0, 1)
    yield vec + (1, 1)
    yield vec + (1, 0)
    yield vec + (1, -1)
    yield vec + (0, -1)
    yield vec + (-1, -1)
    yield vec + (-1, 0)
    yield vec + (-1, 1)


def neigbors_tl_br(vec: "Vec2", include_center=False):
    """Manhattan neighbors inc diagonal, top-left to bottom-right"""
    vec = Vec2(*vec)
    yield vec + (-1, -1)
    yield vec + (0, -1)
    yield vec + (1, -1)
    yield vec + (-1, 0)

    if include_center:
        yield vec

    yield vec + (1, 0)
    yield vec + (-1, 1)
    yield vec + (0, 1)
    yield vec + (1, 1)


def manhattan_neighbors(vec: "Vec2"):
    """Manhattan neighbors, clockwise"""
    vec = Vec2(*vec)
    yield vec + (0, 1)
    yield vec + (1, 0)
    yield vec + (0, -1)
    yield vec + (-1, 0)


def get_min_x(vecs: Iterable["Vec2"]):
    return min(x for x, _ in vecs)


def get_max_x(vecs: Iterable["Vec2"]):
    return max(x for x, _ in vecs)


def get_min_y(vecs: Iterable["Vec2"]):
    return min(y for _, y in vecs)


def get_max_y(vecs: Iterable["Vec2"]):
    return max(y for _, y in vecs)


class Vec2(NamedTuple):
    """2D Vector implementation with basic features"""
    x: int
    y: int

    def __add__(self, other):
        x, y = other
        return Vec2(self.x + x, self.y + y)

    def __sub__(self, other):
        x, y = other
        return Vec2(self.x - x, self.y - y)

    def __mul__(self, other):
        return Vec2(self.x * other, self.y * other)

    def __mod__(self, other: Tuple[int, int]):
        mod_x, mod_y = other
        return Vec2(self.x % mod_x, self.y % mod_y)

    def rotate_degree(self, degree):
        """
        Rotate clockwise
        """
        return self.rotate(math.radians(degree))

    def rotate(self, radian):
        """
        Rotate clockwise
        """
        cos = math.cos(-radian)
        sin = math.sin(-radian)
        x = self.x * cos - self.y * sin
        y = self.x * sin + self.y * cos
        return Vec2(round(x), round(y))

    def degree(self) -> float:
        """
        direction of the vector in degree.
        (counterclockwise start at x axis)
        """
        angle = math.degrees(math.atan2(self.y, self.x))

        return (360 + angle if angle < 0 else angle) % 360

    @staticmethod
    def from_string(value: str):
        x, y = map(int, map(str.strip, value.split(",")))
        return Vec2(x, y)


class Vec3(NamedTuple):
    """3D Vector implementation with basic features"""
    x: int
    y: int
    z: int

    def __add__(self, other):
        x, y, z = other
        return Vec3(self.x + x, self.y + y, self.z + z)

    def __sub__(self, other):
        x, y, z = other
        return Vec3(self.x - x, self.y - y, self.z - z)

    def __mul__(self, other):
        return Vec3(self.x * other, self.y * other, self.z * other)

    def manhattan(self, other: "Vec3"):
        (x1, y1, z1) = self
        (x2, y2, z2) = other
        return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)
