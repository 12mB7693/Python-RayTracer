from src.raytracer import Color, Point, PointLight


def test_point_light_constructor():
    intensity = Color(1, 1, 1)
    position = Point(0, 0, 0)
    light = PointLight(position, intensity)
    assert light.position == position
    assert light.intensity == intensity
