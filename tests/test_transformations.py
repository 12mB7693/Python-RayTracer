import math

from src import (Point, Vector, rotation_x, rotation_y, rotation_z, scaling,
                 shearing, translation)


def test_translation():
    transform = translation(5, -3, 2)
    p = Point(-3, 4, 5)
    assert transform.multiply_tuple(p) == Point(2, 1, 7)


def test_inverse_translation():
    transform = translation(5, -3, 2)
    inv = transform.inverse()
    p = Point(-3, 4, 5)
    assert inv.multiply_tuple(p) == Point(-8, 7, 3)


def test_translation_does_not_transform_vectors():
    transform = translation(5, -3, 2)
    v = Vector(-3, 4, 5)
    assert transform.multiply_tuple(v) == v


def test_scaling_point():
    transform = scaling(2, 3, 4)
    p = Point(-4, 6, 8)
    print(transform.values)
    print(transform.multiply_tuple(p).x)
    assert transform.multiply_tuple(p) == Point(-8, 18, 32)


def test_scaling_vector():
    transform = scaling(2, 3, 4)
    v = Vector(-4, 6, 8)
    print(transform.multiply_tuple(v).x)
    assert transform.multiply_tuple(v) == Vector(-8, 18, 32)


def test_scaling_inverse():
    transform = scaling(2, 3, 4)
    inv = transform.inverse()
    v = Vector(-4, 6, 8)
    assert inv.multiply_tuple(v) == Vector(-2, 2, 2)


def test_scaling_reflection():
    transform = scaling(-1, 1, 1)
    p = Point(2, 3, 4)
    assert transform.multiply_tuple(p) == Point(-2, 3, 4)


def test_rotation_x():
    p = Point(0, 1, 0)
    half_quarter = rotation_x(math.pi / 4)
    full_quarter = rotation_x(math.pi / 2)
    assert half_quarter.multiply_tuple(p) == Point(
        0, math.sqrt(2) / 2, math.sqrt(2) / 2
    )
    assert full_quarter.multiply_tuple(p) == Point(0,0,1)

def test_rotation_x_inverse():
    p = Point(0, 1, 0)
    half_quarter = rotation_x(math.pi / 4)
    inv = half_quarter.inverse()
    assert inv.multiply_tuple(p) == Point(
        0, math.sqrt(2) / 2, - math.sqrt(2) / 2
    )

def test_rotation_y():
    p = Point(0, 0, 1)
    half_quarter = rotation_y(math.pi / 4)
    full_quarter = rotation_y(math.pi / 2)
    print(half_quarter.multiply_tuple(p).x)
    assert half_quarter.multiply_tuple(p) == Point(math.sqrt(2)/2, 0, math.sqrt(2)/2)
    print(full_quarter.multiply_tuple(p).x)
    assert full_quarter.multiply_tuple(p) == Point(1, 0, 0)

def test_rotation_z():
    p = Point(0, 1, 0)
    half_quarter = rotation_z(math.pi / 4)
    full_quarter = rotation_z(math.pi / 2)
    assert half_quarter.multiply_tuple(p) == Point(-math.sqrt(2)/2, math.sqrt(2)/2, 0)
    assert full_quarter.multiply_tuple(p) == Point(-1, 0, 0)


def test_shearing_x_y():
    transform = shearing(1, 0, 0, 0, 0, 0)
    p = Point(2, 3, 4)
    assert transform.multiply_tuple(p) == Point(5, 3, 4)


def test_shearing_x_z():
    transform = shearing(0, 1, 0, 0, 0, 0)
    p = Point(2, 3, 4)
    assert transform.multiply_tuple(p) == Point(6, 3, 4)


def test_shearing_y_x():
    transform = shearing(0, 0, 1, 0, 0, 0)
    p = Point(2, 3, 4)
    assert transform.multiply_tuple(p) == Point(2, 5, 4)


def test_shearing_y_z():
    transform = shearing(0, 0, 0, 1, 0, 0)
    p = Point(2, 3, 4)
    assert transform.multiply_tuple(p) == Point(2, 7, 4)

def test_shearing_z_x():
    transform = shearing(0, 0, 0, 0, 1, 0)
    p = Point(2, 3, 4)
    assert transform.multiply_tuple(p) == Point(2, 3, 6)

def test_shearing_z_y():
    transform = shearing(0, 0, 0, 0, 0, 1)
    p = Point(2, 3, 4)
    assert transform.multiply_tuple(p) == Point(2, 3, 7)


def test_chaining_individual_transformations():
    p = Point(1, 0, 1)
    A = rotation_x(math.pi / 2)
    B = scaling(5, 5, 5)
    C = translation(10, 5, 7)
    # rotation first
    p2 = A.multiply_tuple(p)
    assert p2 == Point(1, -1, 0)
    # then apply scaling
    p3 = B.multiply_tuple(p2)
    assert p3 == Point(5, -5, 0)
    # then apply translation
    p4 = C.multiply_tuple(p3)
    assert p4 == Point(15, 0, 7)


def test_chaining_all_transformations():
    p = Point(1, 0, 1)
    A = rotation_x(math.pi / 2)
    B = scaling(5, 5, 5)
    C = translation(10, 5, 7)
    T = C.multiply_matrix(B.multiply_matrix(A))
    p2 = T.multiply_tuple(p)
    assert p2 == Point(15, 0, 7)
