from src import *

def test_empty_world():
    w = World()
    assert len(w.objects) == 0
    assert w.lightSource is None

def test_default_world():
    w = World.default()
    s1 = Sphere()
    s1.material = Material(color=Color(0.8, 1, 0.6), diffuse=0.7, specular=0.2)
    s2 = Sphere()
    s2.set_transform(scaling(0.5, 0.5, 0.5))
    light = PointLight(Point(-10, 10, -10), Color(1, 1, 1))
    assert [s1.material, s1.transform] in [[s.material, s.transform] for s in w.objects]
    assert [s2.material, s2.transform] in [[s.material, s.transform] for s in w.objects]
    assert light == w.lightSource

def test_intersect_world_with_ray():
    w = World.default()
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    intersections = w.intersect(r)
    assert len(intersections) == 4
    assert intersections[0].t == 4
    assert intersections[1].t == 4.5
    assert intersections[2].t == 5.5
    assert intersections[3].t == 6

def test_shading_intersection():
    w = World.default()
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    shape = w.objects[0]
    i = Intersection(4, shape)
    comps = prepare_computations(i, r)
    c = w.shade_hit(comps)
    assert c == Color(0.38066, 0.47583, 0.2855)

def test_shading_intersection_from_inside():
    w = World.default()
    w.lightSource = PointLight(Point(0, 0.25, 0), Color(1, 1, 1))
    r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
    shape = w.objects[1]
    i = Intersection(0.5, shape)
    comps = prepare_computations(i, r)
    c = w.shade_hit(comps)
    assert c == Color(0.90498, 0.90498, 0.90498)

def test_color_when_ray_misses():
    w = World.default()
    r = Ray(Point(0, 0, -5), Vector(0, 1, 0))
    c = w.color_at(r)
    assert c == Color(0, 0, 0)

def test_color_when_ray_hits():
    w = World.default()
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    c = w.color_at(r)
    assert c == Color(0.38066, 0.47583, 0.2855)

def test_color_when_intersection_behind_ray():
    w = World.default()
    outer = w.objects[0]
    outer.material.ambient = 1
    inner = w.objects[1]
    inner.material.ambient = 1
    r = Ray(Point(0, 0, 0.75), Vector(0, 0 ,-1))
    c = w.color_at(r)
    assert c == inner.material.color
