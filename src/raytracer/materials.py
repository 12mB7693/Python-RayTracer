from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .lights import PointLight

import abc
import math

import numpy as np
from PIL import Image

from . import shapes
from .matrix import create_identity_matrix
from .tuples import Color, Point


class Pattern(metaclass=abc.ABCMeta):
    def __init__(self):
        self.transform = create_identity_matrix()

    @abc.abstractmethod
    def pattern_at(self, point: Point) -> Color:
        pass

    def pattern_at_shape(self, shape: shapes.Shape, world_point: Point) -> Color:
        object_point = shape.transform.inverse().multiply(world_point)
        pattern_point = self.transform.inverse().multiply(object_point)
        return self.pattern_at(pattern_point)


class TexturePath:
    earthTexture = "src/raytracer/textures/world_texture.png"
    horizontalStripes = "src/raytracer/textures/horizontal_stripes.jpg"
    vertical = "src/raytracer/textures/vertical.jpg"


class Texture(Pattern):
    def __init__(self, pathToTexture: TexturePath) -> None:
        image = Image.open(pathToTexture)
        self.texture = np.asarray(image)
        self.u_max, self.v_max, _ = self.texture.shape

    def pattern_at_shape(self, shape: shapes.Shape, world_point: Point) -> Color:
        object_point = shape.transform.inverse().multiply(world_point)
        # if abs(object_point.magnitude() - 1) < 0.001:
        #    return Color(1, 1, 0)
        # if 1 - object_point.z < 0.2:
        #    return Colors.red
        # if 1 - object_point.y < 0.2:
        #    return Colors.blue
        # if 1 - object_point.x < 0.2:
        #    return Colors.green
        v, u = shape.texture_transform(object_point)
        index_u = math.floor(self.u_max * u)
        index_v = math.floor(self.v_max * v)
        color = self.texture[index_u, index_v]
        return Color(color[0] / 255, color[1] / 255, color[2] / 255)

    def pattern_at(self, point):
        return


class StripePattern(Pattern):
    def __init__(self, c1: Color, c2: Color):
        super().__init__()
        self.c1 = c1
        self.c2 = c2

    def pattern_at(self, point: Point) -> Color:
        if math.floor(point.x) % 2 == 0:
            return self.c1
        else:
            return self.c2


class ConstantPattern(Pattern):
    def __init__(self, color: Color):
        super().__init__()
        self.color = color

    def pattern_at(self, point: Point) -> Color:
        return self.color


@dataclass
class Material:
    ambient: float = 0.1
    diffuse: float = 0.9
    specular: float = 0.9
    shininess: float = 200.0
    pattern: Pattern = ConstantPattern(Color(1, 1, 1))

    def __eq__(self, other):
        if isinstance(other, Material):
            return (
                math.isclose(self.ambient, other.ambient, abs_tol=1e-5)
                and math.isclose(self.diffuse, other.diffuse, abs_tol=1e-5)
                and math.isclose(self.specular, other.specular, abs_tol=1e-5)
                and math.isclose(self.shininess, other.shininess, abs_tol=1e-5)
            )
        else:
            return False

    def __repr__(self):
        return f"Material({self.ambient}, {self.diffuse}, {self.specular, {self.shininess}})"


def lighting(
    light: PointLight,
    intersectionInfo: shapes.IntersectionInfo,
    in_shadow: bool = False,
) -> Color:
    shape = intersectionInfo.intersection.shape
    m = shape.material

    color = m.pattern.pattern_at_shape(shape, intersectionInfo.point)

    effective_color = color.hadamard_product(light.intensity)
    lightv = (light.position - intersectionInfo.point).normalize()
    ambient = effective_color * m.ambient

    if in_shadow:
        return ambient

    light_dot_normal = lightv.dot(intersectionInfo.normalv)
    if light_dot_normal < 0:
        diffuse = Color(0, 0, 0)
        specular = Color(0, 0, 0)
    else:
        diffuse = effective_color * m.diffuse * light_dot_normal
        reflectv = -lightv.reflect(intersectionInfo.normalv)
        reflect_dot_eye = reflectv.dot(intersectionInfo.eyev)

        if reflect_dot_eye <= 0:
            specular = Color(0, 0, 0)
        else:
            factor = reflect_dot_eye**m.shininess
            specular = light.intensity * m.specular * factor

    return ambient + diffuse + specular
