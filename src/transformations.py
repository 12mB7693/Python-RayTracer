import math
from .matrix import Matrix, create_identity_matrix


def translation(x: float, y: float, z: float) -> Matrix:
    matrix = create_identity_matrix()
    matrix.set_value_at(0, 3, x)
    matrix.set_value_at(1, 3, y)
    matrix.set_value_at(2, 3, z)
    return matrix


def scaling(x: float, y: float, z: float) -> Matrix:
    matrix = create_identity_matrix()
    matrix.set_value_at(0, 0, x)
    matrix.set_value_at(1, 1, y)
    matrix.set_value_at(2, 2, z)
    return matrix


def rotation_x(radians: float) -> Matrix:
    matrix = create_identity_matrix()
    matrix.set_value_at(1, 1, math.cos(radians))
    matrix.set_value_at(2, 2, math.cos(radians))
    matrix.set_value_at(1, 2, - math.sin(radians))
    matrix.set_value_at(2, 1, math.sin(radians))
    return matrix


def rotation_y(radians: float) -> Matrix:
    matrix = create_identity_matrix()
    matrix.set_value_at(0, 0, math.cos(radians))
    matrix.set_value_at(2, 2, math.cos(radians))
    matrix.set_value_at(0, 2, math.sin(radians))
    matrix.set_value_at(2, 0, - math.sin(radians))
    return matrix

def rotation_z(radians: float) -> Matrix:
    matrix = create_identity_matrix()
    matrix.set_value_at(0, 0, math.cos(radians))
    matrix.set_value_at(1, 1, math.cos(radians))
    matrix.set_value_at(1, 0, math.sin(radians))
    matrix.set_value_at(0, 1, - math.sin(radians))
    return matrix

def shearing(x_y: float, x_z: float, y_x: float, y_z: float, z_x: float, z_y: float) -> Matrix:
    matrix = create_identity_matrix()
    matrix.set_value_at(0, 1, x_y)
    matrix.set_value_at(1, 0, y_x)
    matrix.set_value_at(0, 2, x_z)
    matrix.set_value_at(2, 0, z_x)
    matrix.set_value_at(1, 2, y_z)
    matrix.set_value_at(2, 1, z_y)
    return matrix
