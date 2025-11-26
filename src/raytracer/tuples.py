from __future__ import annotations

import math

ABS_TOL = 1e-5


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
                math.isclose(self.x, value.x, abs_tol=ABS_TOL)
                and math.isclose(self.y, value.y, abs_tol=ABS_TOL)
                and math.isclose(self.z, value.z, abs_tol=ABS_TOL)
                and math.isclose(self.w, value.w, abs_tol=ABS_TOL)
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

    def reflect(self, normal: Vector) -> Vector:
        return self - normal * 2 * self.dot(normal)

    # def __repr__(self):
    #    return f"Tuple({self.x}, {self.y}, {self.z}, {self.w})"


class Color:
    def __init__(self, red: float, green: float, blue: float):
        self.red = red
        self.green = green
        self.blue = blue

    # __slots__ = ()
    # WHITE = Color(1, 1, 1)

    # @property
    # def white(self):
    #    return Color(1, 1, 1)

    # @property
    # def black(self):
    #    return Color(0, 0, 0)

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Color):
            return (
                math.isclose(self.red, value.red, abs_tol=ABS_TOL)
                and math.isclose(self.green, value.green, abs_tol=ABS_TOL)
                and math.isclose(self.blue, value.blue, abs_tol=ABS_TOL)
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

    def __mul__(self, value):
        if isinstance(value, int) or isinstance(value, float):
            return Color(self.red * value, self.green * value, self.blue * value)
        elif isinstance(value, Color):
            raise Exception(
                "The value is not a scalar, but a color. Did you mean to use hadamard_product?"
            )
        else:
            raise Exception

    __rmul__ = __mul__

    def hadamard_product(self, other: Color):
        return Color(
            self.red * other.red, self.green * other.green, self.blue * other.blue
        )

    def __repr__(self):
        return f"Color({self.red}, {self.green}, {self.blue})"


class Colors:
    white = Color(1, 1, 1)
    black = Color(0, 0, 0)
    red = Color(1, 0, 0)
    green = Color(0, 1, 0)
    blue = Color(0, 0, 1)


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
