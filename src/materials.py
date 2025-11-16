from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .lights import PointLight

from .tuples import Color, Vector, Point


import math

class Material:

    def __init__(self):
        self.color = Color(1, 1, 1)
        self.ambient = 0.1
        self.diffuse = 0.9
        self.specular = 0.9
        self.shininess = 200.0

    def __eq__(self, other):
        if isinstance(other, Material):
            return (
                self.color == other.color
                and math.isclose(self.ambient, other.ambient, abs_tol=1e-5)
                and math.isclose(self.diffuse, other.diffuse, abs_tol=1e-5)
                and math.isclose(self.specular, other.specular, abs_tol=1e-5)
                and math.isclose(self.shininess, other.shininess, abs_tol=1e-5)
            )
        else:
            return False

    def __repr__(self):
        return f"Material({self.color}, {self.ambient}, {self.diffuse}, {self.specular, {self.shininess}})"

def lighting(m: Material, light: PointLight, position: Point, eyev: Vector, normalv: Vector) -> Color:
    effective_color = m.color * light.intensity
    lightv = (light.position - position).normalize()
    ambient = effective_color * m.ambient
    light_dot_normal = lightv.dot(normalv)

    if light_dot_normal < 0:
        diffuse = Color(0, 0, 0)
        specular = Color(0, 0, 0)
    else:
        diffuse = effective_color * m.diffuse * light_dot_normal
        reflectv = -lightv.reflect(normalv)
        reflect_dot_eye = reflectv.dot(eyev)

        if reflect_dot_eye <= 0:
            specular = Color(0, 0, 0)
        else:
            factor = reflect_dot_eye**m.shininess
            specular = light.intensity * m.specular * factor

    return ambient + diffuse + specular
