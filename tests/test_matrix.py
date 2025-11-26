import math

from src.raytracer import Matrix, Tuple, create_identity_matrix


def test_matrix():
    values = [
        1,
        2,
        3,
        4,
        5.5,
        6.5,
        7.5,
        8.5,
        9,
        10,
        11,
        12,
        13.5,
        14.5,
        15.5,
        16.5,
    ]
    matrix = Matrix(values)
    assert matrix.get_value_at(0, 0) == 1
    assert matrix.get_value_at(0, 3) == 4
    assert matrix.get_value_at(1, 0) == 5.5
    assert matrix.get_value_at(1, 2) == 7.5
    assert matrix.get_value_at(2, 2) == 11
    assert matrix.get_value_at(3, 0) == 13.5
    assert matrix.get_value_at(3, 2) == 15.5


def test_matrix_dimension_two():
    matrix = Matrix([-3, 5, 1, -2], dimension=2)
    # matrix.set_value_at(0, 0, -3)
    # matrix.set_value_at(0, 1, 5)
    # matrix.set_value_at(1, 0, 1)
    # m#atrix.set_value_at(1, 1, -2)
    assert matrix.get_value_at(0, 0) == -3
    assert matrix.get_value_at(0, 1) == 5
    assert matrix.get_value_at(1, 0) == 1
    assert matrix.get_value_at(1, 1) == -2


def test_matrix_dimension_three():
    matrix = Matrix([-3, 5, 0, 1, -2, -7, 0, 1, 1], dimension=3)
    assert matrix.get_value_at(0, 0) == -3
    assert matrix.get_value_at(1, 1) == -2
    assert matrix.get_value_at(2, 2) == 1


def test_matrix_equality():
    matrix1 = Matrix(
        values=[1, 2, 3, 4, 5.5, 6.5, 7.5, 8.5, 9, 10, 11, 12, 13.5, 14.5, 15.5, 16.5]
    )
    matrix2 = Matrix(
        values=[1, 2, 3, 4, 5.5, 6.5, 7.5, 8.5, 9, 10, 11, 12, 13.5, 14.5, 15.5, 16.5]
    )
    assert matrix1 == matrix2


def test_matrix_inequality():
    matrix1 = Matrix(
        values=[1, 2, 3, 4, 5.5, 6.5, 7.5, 8, 9, 10, 11, 12, 13.5, 14.5, 15.5, 16.5]
    )
    matrix2 = Matrix(
        values=[1, 2, 3, 4, 5.5, 6.5, 7.5, 8.5, 9, 10, 11, 12, 13.5, 14.5, 15.5, 16.5]
    )
    assert matrix1 != matrix2


def test_matrix_multiplication():
    matrix1 = Matrix(values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 4, 3, 2])
    matrix2 = Matrix(values=[-2, 1, 2, 3, 3, 2, 1, -1, 4, 3, 6, 5, 1, 2, 7, 8])
    result = matrix1.multiply_matrix(matrix2)
    expected = Matrix(
        values=[20, 22, 50, 48, 44, 54, 114, 108, 40, 58, 110, 102, 16, 26, 46, 42]
    )
    assert result == expected


def test_tuple_multiplication():
    matrix = Matrix([1, 2, 3, 4, 2, 4, 4, 2, 8, 6, 4, 1, 0, 0, 0, 1])
    tuple = Tuple(1, 2, 3, 1)
    result = matrix.multiply_tuple(tuple)
    expected = Tuple(18, 24, 33, 1)
    assert result == expected


def test_identity():
    matrix = Matrix(values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 4, 3, 2])
    assert matrix.multiply_matrix(create_identity_matrix()) == matrix


def test_transpose():
    matrix = Matrix([0, 9, 3, 0, 9, 8, 0, 8, 1, 8, 5, 3, 0, 0, 5, 8])
    expected = Matrix([0, 9, 1, 0, 9, 8, 8, 0, 3, 0, 5, 5, 0, 8, 3, 8])
    assert expected == matrix.transpose()


def test_transpose_identity():
    assert create_identity_matrix() == create_identity_matrix().transpose()


def test_determinant_dimension_two():
    matrix = Matrix(values=[1, 5, -3, 2], dimension=2)
    # matrix.set_value_at(0, 0, 1)
    # matrix.set_value_at(0, 1, 5)
    # matrix.set_value_at(1, 0, -3)
    # matrix.set_value_at(1, 1, 2)
    assert matrix.determinant() == 17


"""
def test_submatrix1():
    matrix = Matrix(dimension=3, values=[1, 5, 0, -3, 2, 7, 0, 6, -3])
    submatrix = matrix.submatrix(0, 2)
    assert submatrix == Matrix(dimension=2, values=[-3, 2, 0, 6])


def test_submatrix2():
    matrix = Matrix(
        dimension=4, values=[-6, 1, 1, 6, -8, 5, 8, 6, -1, 0, 8, 2, -7, 1, -1, 1]
    )
    submatrix = matrix.submatrix(2, 1)
    assert submatrix == Matrix(dimension=3, values=[-6, 1, 6, -8, 8, 6, -7, -1, 1])


def test_minor():
    matrix = Matrix(dimension=3, values=[3, 5, 0, 2, -1, -7, 6, -1, 5])
    submatrix = matrix.submatrix(1, 0)
    assert submatrix.determinant() == 25
    assert matrix.minor(1, 0) == 25


def test_cofactor():
    matrix = Matrix(dimension=3, values=[3, 5, 0, 2, -1, -7, 6, -1, 5])
    assert matrix.minor(0, 0) == -12
    assert matrix.cofactor(0, 0) == -12
    assert matrix.minor(1, 0) == 25
    assert matrix.cofactor(1, 0) == -25
"""


def test_determinant_three_dimensional():
    matrix = Matrix(dimension=3, values=[1, 2, 6, -5, 8, -4, 2, 6, 4])
    # assert matrix.cofactor(0, 0) == 56
    # assert matrix.cofactor(0, 1) == 12
    # assert matrix.cofactor(0, 2) == -46
    assert math.isclose(matrix.determinant(), -196.0)


def test_determinant_four_dimensional():
    matrix = Matrix(
        dimension=4, values=[-2, -8, 3, 5, -3, 1, 7, 3, 1, 2, -9, 6, -6, 7, 7, -9]
    )
    # assert matrix.cofactor(0, 0) == 690
    # assert matrix.cofactor(0, 1) == 447
    # assert matrix.cofactor(0, 2) == 210
    # assert matrix.cofactor(0, 3) == 51
    assert math.isclose(matrix.determinant(), -4071)


def test_is_invertible():
    matrix = Matrix(values=[6, 4, 4, 4, 5, 5, 7, 6, 4, -9, 3, -7, 9, 1, 7, -6])
    assert matrix.is_invertible() is True


def test_is_not_invertible():
    matrix = Matrix(values=[-4, 2, -2, -3, 9, 6, 2, 6, 0, -5, 1, -5, 0, 0, 0, 0])
    assert matrix.is_invertible() is False


def test_inverse():
    matrix = Matrix(values=[-5, 2, 6, -8, 1, -5, 1, 8, 7, 7, -6, -7, 1, -3, 7, 4])
    inverse = matrix.inverse()
    assert math.isclose(matrix.determinant(), 532)
    # assert matrix.cofactor(2, 3) == -160
    assert math.isclose(inverse.get_value_at(3, 2), -160.0 / 532.0)
    # assert matrix.cofactor(3, 2) == 105
    assert math.isclose(inverse.get_value_at(2, 3), 105 / 532)
    expected = Matrix(
        values=[
            0.21805,
            0.45113,
            0.24060,
            -0.04511,
            -0.80827,
            -1.45677,
            -0.44361,
            0.52256,
            -0.07895,
            -0.22368,
            -0.05263,
            0.19737,
            -0.52068,
            -0.81391,
            -0.30075,
            0.30639,
        ]
    )
    assert expected.approximately_equals(inverse)


def test_multiply_by_its_inverse():
    matrix = Matrix(values=[6, 4, 4, 4, 5, 5, 7, 6, 4, -9, 3, -7, 9, 1, 7, -6])
    inverse = matrix.inverse()
    assert inverse.multiply_matrix(matrix).approximately_equals(
        create_identity_matrix()
    )
