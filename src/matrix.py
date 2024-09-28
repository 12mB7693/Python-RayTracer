from __future__ import annotations
import math
from .tuples import Tuple


class Matrix:
    def __init__(self, values: list[float] | None = None, dimension: int = 4) -> None:
        self.dimension = dimension
        self.size = 4
        if values is None:
            self.values = [0.0 for i in range(self.size * self.size)]
        else:
            if len(values) == self.size * self.size:
                self.values = values
            elif len(values) == self.dimension * self.dimension:
                self.values = [0.0 for i in range(self.size * self.size)]
                for row in range(self.dimension):
                    for column in range(self.dimension):
                        self.values[row * self.size + column] = values[
                            row * self.dimension + column
                        ]

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Matrix):
            return (
                all(
                    [
                        math.isclose(self.values[i], other.values[i])
                        for i in range(self.size * self.size)
                    ]
                )
                and self.dimension == other.dimension
            )
        else:
            return False

    def approximately_equals(self, other: object, tolerance=0.01) -> bool:
        if isinstance(other, Matrix):
            return (
                all(
                    [
                        math.isclose(self.values[i], other.values[i], abs_tol=tolerance)
                        for i in range(self.size * self.size)
                    ]
                )
                and self.dimension == other.dimension
            )
        else:
            return False

    def get_value_at(self, row: int, column: int) -> float:
        return self.values[row * self.size + column]

    def set_value_at(self, row: int, column: int, value: float) -> None:
        self.values[row * self.size + column] = value

    def _get_row(self, row_index: int) -> Tuple:
        return Tuple(
            self.get_value_at(row_index, 0),
            self.get_value_at(row_index, 1),
            self.get_value_at(row_index, 2),
            self.get_value_at(row_index, 3),
        )

    def _get_column(self, column_index: int) -> Tuple:
        return Tuple(
            self.get_value_at(0, column_index),
            self.get_value_at(1, column_index),
            self.get_value_at(2, column_index),
            self.get_value_at(3, column_index),
        )

    def multiply_matrix(self, other: Matrix) -> Matrix:
        rows = [self._get_row(i) for i in range(self.size)]
        columns = [other._get_column(i) for i in range(self.size)]
        result = Matrix()
        for row in range(self.size):
            for column in range(self.size):
                result.set_value_at(row, column, rows[row].dot(columns[column]))
        return result

    def multiply_tuple(self, other: Tuple) -> Tuple:
        rows = [self._get_row(i) for i in range(self.size)]
        result = Tuple(
            rows[0].dot(other),
            rows[1].dot(other),
            rows[2].dot(other),
            rows[3].dot(other),
        )
        return result

    def transpose(self) -> Matrix:
        matrix = Matrix()
        for i in range(self.size):
            for j in range(self.size):
                matrix.set_value_at(i, j, self.get_value_at(j, i))
        return matrix

    def determinant(self) -> float:
        det = 0.0
        if self.dimension == 2:
            det = self.get_value_at(0, 0) * self.get_value_at(1, 1) - self.get_value_at(
                0, 1
            ) * self.get_value_at(1, 0)
        elif self.dimension > 2:
            first_row = self._get_row(0)
            det += first_row.x * self.cofactor(0, 0)
            det += first_row.y * self.cofactor(0, 1)
            det += first_row.z * self.cofactor(0, 2)
            det += first_row.w * self.cofactor(0, 3)
        return det

    def submatrix(self, row: int, column: int) -> Matrix:
        submatrix = Matrix(dimension=self.dimension - 1)
        for i in range(submatrix.dimension):
            for j in range(submatrix.dimension):
                old_i = i
                old_j = j
                if i >= row:
                    old_i = i + 1
                if j >= column:
                    old_j = j + 1
                value = self.get_value_at(old_i, old_j)
                submatrix.set_value_at(i, j, value)
        return submatrix

    def minor(self, row: int, column: int) -> float:
        return self.submatrix(row, column).determinant()

    def cofactor(self, row: int, column: int) -> float:
        factor = math.pow(-1, row + column)
        return factor * self.minor(row, column)

    def is_invertible(self) -> bool:
        return not math.isclose(0.0, self.determinant())

    def inverse(self) -> Matrix | None:
        if not self.is_invertible():
            return None
        inverse = Matrix(dimension=self.dimension)
        for row in range(self.dimension):
            for col in range(self.dimension):
                c = self.cofactor(row, col)
                inverse.set_value_at(col, row, c / self.determinant())
        print(inverse.values)
        return inverse


def create_identity_matrix():
    identity_matrix = Matrix([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])
    return identity_matrix
