from src.tuples import Tuple, Vector, Point, create_tuple
import math


def test_create_point():
    point = create_tuple(4.3, -4.2, 3.1, 1.0)
    assert isinstance(point, Point)
    assert not isinstance(point, Vector)
    assert point.x == 4.3
    assert point.y == -4.2
    assert point.z == 3.1
    assert point.w == 1


def test_create_vector():
    vector = create_tuple(4.3, -4.2, 3.1, 0.0)
    assert isinstance(vector, Vector)
    assert not isinstance(vector, Point)
    assert vector.x == 4.3
    assert vector.y == -4.2
    assert vector.z == 3.1
    assert vector.w == 0


def test_point_creates_tuple():
    point = Point(4, -4, 3)
    assert point == Tuple(4, -4, 3, 1)


def test_vector_creates_tuple():
    vector = Vector(4, -4, 3)
    assert vector == Tuple(4, -4, 3, 0)


def test_add_tuples():
    tuple1 = Tuple(3, -2, 5, 1)
    tuple2 = Tuple(-2, 3, 1, 0)
    assert tuple1 + tuple2 == Tuple(1, 1, 6, 1)


def test_subtract_point_point():
    p1 = Point(3, 2, 1)
    p2 = Point(5, 6, 7)
    assert p1 - p2 == Vector(-2, -4, -6)


def test_subtract_point_vector():
    p = Point(3, 2, 1)
    v = Vector(5, 6, 7)
    assert p - v == Point(-2, -4, -6)


def test_subtract_vector_vector():
    v1 = Vector(3, 2, 1)
    v2 = Vector(5, 6, 7)
    assert v1 - v2 == Vector(-2, -4, -6)


def test_subtract_vector_from_zero():
    zero = Vector(0, 0, 0)
    v = Vector(1, -2, 3)
    assert zero - v == Vector(-1, 2, -3)


def test_negate_tuple():
    a = Tuple(1, -2, 3, -4)
    assert -a == Tuple(-1, 2, -3, 4)


def test_multiply_by_a_scalar():
    a = Tuple(1, -2, 3, -4)
    assert a * 3.5 == Tuple(3.5, -7, 10.5, -14)
    assert 3.5 * a == Tuple(3.5, -7, 10.5, -14)


def test_multiply_by_a_fraction():
    a = Tuple(1, -2, 3, -4)
    assert a * 0.5 == Tuple(0.5, -1, 1.5, -2)


def test_division():
    a = Tuple(1, -2, 3, -4)
    assert a / 2 == Tuple(0.5, -1, 1.5, -2)


def test_magnitude_unit_vector():
    v1 = Vector(1, 0, 0)
    v2 = Vector(0, 1, 0)
    v3 = Vector(0, 0, 1)
    assert v1.magnitude() == 1
    assert v2.magnitude() == 1
    assert v3.magnitude() == 1


def test_magnitude_vector():
    v1 = Vector(1, 2, 3)
    v2 = Vector(-1, -2, -3)
    assert math.isclose(v1.magnitude(), math.sqrt(14))
    assert math.isclose(v2.magnitude(), math.sqrt(14))


def test_normalize_vector():
    v1 = Vector(4, 0, 0)
    v2 = Vector(1, 2, 3)
    assert v1.normalize() == Vector(1, 0, 0)
    assert v2.normalize() == Vector(
        1 / math.sqrt(14), 2 / math.sqrt(14), 3 / math.sqrt(14)
    )
    assert v2.normalize().magnitude() == 1


def test_dot_product():
    a = Vector(1, 2, 3)
    b = Vector(2, 3, 4)
    assert a.dot(b) == 20


def test_cross_product():
    a = Vector(1, 2, 3)
    b = Vector(2, 3, 4)
    assert a.cross(b) == Vector(-1, 2, -1)
    assert b.cross(a) == Vector(1, -2, 1)
