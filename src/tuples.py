from __future__ import annotations
import math


class Tuple:
    def __init__(self, x, y, z, w) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    # create method
    def create(self, x, y, z, w):
        return Tuple(x, y, z, w)

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Tuple):
            return (
                math.isclose(self.x, value.x, abs_tol=1e-9)
                and math.isclose(self.y, value.y, abs_tol=1e-9)
                and math.isclose(self.z, value.z, abs_tol=1e-9)
                and math.isclose(self.w, value.w, abs_tol=1e-9)
            )
        else:
            return False

    def __add__(self, other: Tuple):
        return self.create(
            self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w
        )

    def __sub__(self, other):
        return Tuple(
            self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w
        )

    def __neg__(self):
        return Tuple(-self.x, -self.y, -self.z, -self.w)

    def __mul__(self, scalar):
        return Tuple(self.x * scalar, self.y * scalar, self.z * scalar, self.w * scalar)

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        return Tuple(self.x / scalar, self.y / scalar, self.z / scalar, self.w / scalar)

    def magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self):
        return Vector(
            self.x / self.magnitude(),
            self.y / self.magnitude(),
            self.z / self.magnitude(),
        )

    def dot(self, other: Tuple) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z + self.w * other.w

    def cross(self, other: Vector) -> Vector:
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )


class Color:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Color):
            return (
                math.isclose(self.red, value.red)
                and math.isclose(self.green, value.green)
                and math.isclose(self.blue, value.blue)
            )
        else:
            return False

    def __add__(self, other):
        return Color(
            self.red + other.red, self.green + other.green, self.blue + other.blue
        )

    def __sub__(self, other):
        return Color(
            self.red - other.red, self.green - other.green, self.blue - other.blue
        )

    def __mul__(self, scalar):
        return Color(self.red * scalar, self.green * scalar, self.blue * scalar)

    __rmul__ = __mul__

    def hadamard_product(self, other):
        return Color(
            self.red * other.red, self.green * other.green, self.blue * other.blue
        )


class Vector(Tuple):
    def __init__(self, x: float, y: float, z: float) -> None:
        super().__init__(x, y, z, 0)

    # def create(x, y, z, w):
    #    return Vector(x, y, z)


class Point(Tuple):
    def __init__(self, x, y, z) -> None:
        super().__init__(x, y, z, 1)


def create_tuple(x, y, z, w):
    if w == 0:
        return Vector(x, y, z)
    elif w == 1:
        return Point(x, y, z)
    else:
        return None
