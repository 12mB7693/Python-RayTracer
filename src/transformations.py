import math
from .matrix import Matrix, create_identity_matrix
from .tuples import Point, Vector


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

def view_transform(eye_origin: Point, to: Point, up: Vector) -> Matrix:
    """
    :param Point eye_origin:  specifies where the viewer (the eye) is in the scene
    :param Point to: specifies the point in the scene at which we want to look
    :param Vector up: indicates which direction is up
    """
    forward = (to - eye_origin).normalize()
    left = forward.cross(up.normalize())
    true_up = left.cross(forward)
    orientation = [left.x, left.y, left.z, 0, true_up.x, true_up.y, true_up.z, 0,
                   -forward.x, -forward.y, -forward.z, 0, 0, 0, 0, 1]
    return Matrix(values = orientation).multiply(translation(-eye_origin.x, -eye_origin.y, -eye_origin.z))
