from src.raytracer import (Intersection, Point, Ray, Sphere, Vector,
                           create_identity_matrix, hit, scaling, translation)


def test_ray_attributes():
    origin = Point(1, 2, 3)
    direction = Vector(4, 5, 6)
    ray = Ray(origin, direction)
    assert ray.origin == origin
    assert ray.direction == direction


def test_ray_position():
    ray = Ray(Point(2, 3, 4), Vector(1, 0, 0))
    assert ray.position(0) == Point(2, 3, 4)
    assert ray.position(1) == Point(3, 3, 4)
    assert ray.position(-1) == Point(1, 3, 4)
    assert ray.position(2.5) == Point(4.5, 3, 4)


def test_ray_sphere_intersection():
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    s = Sphere()
    xs = s.intersect(r)
    assert len(xs) == 2
    assert xs[0].t == 4.0
    assert xs[1].t == 6.0
    assert xs[0].shape == s
    assert xs[1].shape == s


def test_intersection():
    s = Sphere()
    i = Intersection(3.5, s)
    assert i.t == 3.5
    assert i.shape == s


def test_intersections():
    s = Sphere()
    i1 = Intersection(1, s)
    i2 = Intersection(2, s)
    xs = [i1, i2]
    assert len(xs) == 2
    assert xs[0].t == 1
    assert xs[1].t == 2


def test_sphere_default_transform():
    s = Sphere()
    assert s.transform == create_identity_matrix()


def test_sphere_set_transform_translation():
    s = Sphere()
    t = translation(2, 3, 4)
    s.set_transform(t)
    assert s.transform == t


def test_sphere_transform_before_intersecting():
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    s = Sphere()
    t = scaling(2, 2, 2)
    s.set_transform(t)
    xs = s.intersect(r)
    assert len(xs) == 2
    assert xs[0].t == 3
    assert xs[1].t == 7


def test_intersect_translated_sphere():
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    s = Sphere()
    t = translation(5, 0, 0)
    s.set_transform(t)
    xs = s.intersect(r)
    assert len(xs) == 0


def test_hit_when_all_intersections_have_positive_t():
    s = Sphere()
    i1 = Intersection(1, s)
    i2 = Intersection(2, s)
    xs = [i2, i1]
    i = hit(xs)
    assert i == i1


def test_hit_when_some_intersections_have_negative_t():
    s = Sphere()
    i1 = Intersection(-1, s)
    i2 = Intersection(1, s)
    xs = [i2, i1]
    i = hit(xs)
    assert i == i2


def test_hit_when_all_intersections_have_negative_t():
    s = Sphere()
    i1 = Intersection(-1, s)
    i2 = Intersection(-2, s)
    xs = [i2, i1]
    i = hit(xs)
    assert i is None


def test_hit_is_lowest_non_negative_t():
    s = Sphere()
    i1 = Intersection(5, s)
    i2 = Intersection(7, s)
    i3 = Intersection(-3, s)
    i4 = Intersection(2, s)
    xs = [i1, i2, i3, i4]
    i = hit(xs)
    assert i == i4


def test_ray_translation():
    r = Ray(Point(1, 2, 3), Vector(0, 1, 0))
    m = translation(3, 4, 5)
    r2 = m.multiply(r)
    assert r2.origin == Point(4, 6, 8)
    assert r2.direction == Vector(0, 1, 0)


def test_ray_scaling():
    r = Ray(Point(1, 2, 3), Vector(0, 1, 0))
    m = scaling(2, 3, 4)
    r2 = m.multiply(r)
    assert r2.origin == Point(2, 6, 12)
    assert r2.direction == Vector(0, 3, 0)
