import math

from src.raytracer import (Color, Colors, ConstantPattern, Intersection,
                           IntersectionInfo, Material, Point, PointLight,
                           Sphere, StripePattern, Vector, lighting, scaling,
                           translation)


def test_material_constructor():
    m = Material()
    assert isinstance(m.pattern, ConstantPattern)
    assert m.pattern.color == Color(1, 1, 1)
    assert m.ambient == 0.1
    assert m.diffuse == 0.9
    assert m.specular == 0.9
    assert m.shininess == 200.0


def test_lighting_eye_btw_light_and_surface():
    pos = Point(0, 0, 0)
    eyev = Vector(0, 0, -1)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 0, -10), Color(1, 1, 1))
    info = IntersectionInfo(Intersection(0, Sphere()), pos, eyev, normalv, False, None)
    result = lighting(light, info)
    assert result == Color(1.9, 1.9, 1.9)


def test_lighting_eye_btw_light_and_surface_eye_offset_45():
    pos = Point(0, 0, 0)
    eyev = Vector(0, 1 / math.sqrt(2), -1 / math.sqrt(2))
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 0, -10), Color(1, 1, 1))
    info = IntersectionInfo(Intersection(0, Sphere()), pos, eyev, normalv, False, None)
    result = lighting(light, info)
    assert result == Color(1.0, 1.0, 1.0)


def test_lighting_eye_opposite_surface_light_offset_45():
    pos = Point(0, 0, 0)
    eyev = Vector(0, 0, -1)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 10, -10), Color(1, 1, 1))
    info = IntersectionInfo(Intersection(0, Sphere()), pos, eyev, normalv, False, None)
    result = lighting(light, info)
    assert result == Color(0.7364, 0.7364, 0.7364)


def test_lighting_eye_in_path_of_reflection_vector():
    pos = Point(0, 0, 0)
    eyev = Vector(0, -1 / math.sqrt(2), -1 / math.sqrt(2))
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 10, -10), Color(1, 1, 1))
    info = IntersectionInfo(Intersection(0, Sphere()), pos, eyev, normalv, False, None)
    result = lighting(light, info)
    assert result == Color(1.6364, 1.6364, 1.6364)


def test_lighting_with_light_behind_surface():
    pos = Point(0, 0, 0)
    eyev = Vector(0, 0, -1)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 0, 10), Color(1, 1, 1))
    info = IntersectionInfo(Intersection(0, Sphere()), pos, eyev, normalv, False, None)
    result = lighting(light, info)
    assert result == Color(0.1, 0.1, 0.1)


def test_lighting_with_surface_in_shadow():
    pos = Point(0, 0, 0)
    eyev = Vector(0, 0, -1)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 0, -10), Color(1, 1, 1))
    in_shadow = True
    info = IntersectionInfo(Intersection(0, Sphere()), pos, eyev, normalv, False, None)
    result = lighting(light, info, in_shadow)
    assert result == Color(0.1, 0.1, 0.1)


def test_lighting_with_a_pattern():
    m = Material(
        ambient=1,
        diffuse=0,
        specular=0,
        pattern=StripePattern(Colors.white, Colors.black),
    )
    eyev = Vector(0, 0, -1)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 0, -10), Color(1, 1, 1))
    s = Sphere()
    s.material = m
    info = IntersectionInfo(Intersection(0.0, s), None, eyev, normalv, False, None)

    info.point = Point(0.9, 0, 0)
    c1 = lighting(light, info)
    info.point = Point(1.1, 0, 0)
    c2 = lighting(light, info)

    assert c1 == Colors.white
    assert c2 == Colors.black


def test_stripe_pattern():
    pattern = StripePattern(Colors.white, Colors.black)
    assert pattern.c1 == Colors.white
    assert pattern.c2 == Colors.black


def test_stripe_pattern_constant_in_y():
    pattern = StripePattern(Colors.white, Colors.black)
    assert pattern.pattern_at(Point(0, 0, 0)) == Colors.white
    assert pattern.pattern_at(Point(0, 1, 0)) == Colors.white
    assert pattern.pattern_at(Point(0, 2, 0)) == Colors.white


def test_stripe_pattern_constant_in_z():
    pattern = StripePattern(Colors.white, Colors.black)
    assert pattern.pattern_at(Point(0, 0, 0)) == Colors.white
    assert pattern.pattern_at(Point(0, 0, 1)) == Colors.white
    assert pattern.pattern_at(Point(0, 0, 2)) == Colors.white


def test_stripe_pattern_alternates_in_x():
    pattern = StripePattern(Colors.white, Colors.black)
    assert pattern.pattern_at(Point(0, 0, 0)) == Colors.white
    assert pattern.pattern_at(Point(0.9, 0, 0)) == Colors.white
    assert pattern.pattern_at(Point(1, 0, 0)) == Colors.black
    assert pattern.pattern_at(Point(-0.1, 0, 0)) == Colors.black
    assert pattern.pattern_at(Point(-1, 0, 0)) == Colors.black
    assert pattern.pattern_at(Point(-1.1, 0, 0)) == Colors.white


def test_stripes_with_object_transformation():
    s = Sphere()
    s.set_transform(scaling(2, 2, 2))
    pattern = StripePattern(Colors.white, Colors.black)
    c = pattern.pattern_at_shape(s, Point(1.5, 0, 0))
    assert c == Colors.white


def test_stripes_with_pattern_transformation():
    s = Sphere()
    pattern = StripePattern(Colors.white, Colors.black)
    pattern.transform = scaling(2, 2, 2)
    c = pattern.pattern_at_shape(s, Point(1.5, 0, 0))
    assert c == Colors.white


def test_stripes_with_both_object_and_pattern_transformation():
    s = Sphere()
    s.set_transform(scaling(2, 2, 2))
    pattern = StripePattern(Colors.white, Colors.black)
    pattern.transform = translation(0.5, 0, 0)
    c = pattern.pattern_at_shape(s, Point(2.5, 0, 0))
    assert c == Colors.white
