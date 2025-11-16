from src import Material, Color
from src import Point, Vector, PointLight, lighting
import math

def test_material_constructor():
    m = Material()
    assert m.color == Color(1, 1, 1)
    assert m.ambient == 0.1
    assert m.diffuse == 0.9
    assert m.specular == 0.9
    assert m.shininess == 200.0

def test_lighting_eye_btw_light_and_surface():
    m = Material()
    pos = Point(0, 0, 0)
    eyev = Vector(0, 0, -1)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 0, -10), Color(1, 1, 1))
    result = lighting(m, light, pos, eyev, normalv)
    assert result == Color(1.9, 1.9, 1.9)


def test_lighting_eye_btw_light_and_surface_eye_offset_45():
    m = Material()
    pos = Point(0, 0, 0)
    eyev = Vector(0, 1/math.sqrt(2), -1/math.sqrt(2))
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 0, -10), Color(1, 1, 1))
    result = lighting(m, light, pos, eyev, normalv)
    assert result == Color(1.0, 1.0, 1.0)

def test_lighting_eye_opposite_surface_light_offset_45():
    m = Material()
    pos = Point(0, 0, 0)
    eyev = Vector(0, 0, -1)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 10, -10), Color(1, 1, 1))
    result = lighting(m, light, pos, eyev, normalv)
    assert result == Color(0.7364, 0.7364, 0.7364)

def test_lighting_eye_in_path_of_reflection_vector():
    m = Material()
    pos = Point(0, 0, 0)
    eyev = Vector(0, -1/math.sqrt(2), -1/math.sqrt(2))
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 10, -10), Color(1, 1, 1))
    result = lighting(m, light, pos, eyev, normalv)
    assert result == Color(1.6364, 1.6364, 1.6364)

def test_lighting_with_light_behind_surface():
    m = Material()
    pos = Point(0, 0, 0)
    eyev = Vector(0, 0, -1)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 0, 10), Color(1, 1, 1))
    result = lighting(m, light, pos, eyev, normalv)
    assert result == Color(0.1, 0.1, 0.1)
