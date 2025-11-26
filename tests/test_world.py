import raytracer as rt


def test_empty_world():
    w = rt.World()
    assert len(w.objects) == 0
    assert w.lightSource is None


def test_default_world():
    w = rt.World.default()
    s1 = rt.Sphere()
    s1.material = rt.Material(
        pattern=rt.ConstantPattern(rt.Color(0.8, 1, 0.6)), diffuse=0.7, specular=0.2
    )
    s2 = rt.Sphere()
    s2.set_transform(rt.scaling(0.5, 0.5, 0.5))
    light = rt.PointLight(rt.Point(-10, 10, -10), rt.Color(1, 1, 1))
    assert [s1.material, s1.transform] in [[s.material, s.transform] for s in w.objects]
    assert [s2.material, s2.transform] in [[s.material, s.transform] for s in w.objects]
    assert light == w.lightSource


def test_intersect_world_with_ray():
    w = rt.World.default()
    r = rt.Ray(rt.Point(0, 0, -5), rt.Vector(0, 0, 1))
    intersections = w.intersect(r)
    assert len(intersections) == 4
    assert intersections[0].t == 4
    assert intersections[1].t == 4.5
    assert intersections[2].t == 5.5
    assert intersections[3].t == 6


def test_shading_intersection():
    w = rt.World.default()
    r = rt.Ray(rt.Point(0, 0, -5), rt.Vector(0, 0, 1))
    shape = w.objects[0]
    i = rt.Intersection(4, shape)
    comps = rt.prepare_computations(i, r)
    c = w.shade_hit(comps)
    assert c == rt.Color(0.38066, 0.47583, 0.2855)


def test_shading_intersection_from_inside():
    w = rt.World.default()
    w.lightSource = rt.PointLight(rt.Point(0, 0.25, 0), rt.Color(1, 1, 1))
    r = rt.Ray(rt.Point(0, 0, 0), rt.Vector(0, 0, 1))
    shape = w.objects[1]
    i = rt.Intersection(0.5, shape)
    comps = rt.prepare_computations(i, r)
    c = w.shade_hit(comps)
    assert c == rt.Color(0.90498, 0.90498, 0.90498)


def test_color_when_ray_misses():
    w = rt.World.default()
    r = rt.Ray(rt.Point(0, 0, -5), rt.Vector(0, 1, 0))
    c = w.color_at(r)
    assert c == rt.Color(0, 0, 0)


def test_color_when_ray_hits():
    w = rt.World.default()
    r = rt.Ray(rt.Point(0, 0, -5), rt.Vector(0, 0, 1))
    c = w.color_at(r)
    assert c == rt.Color(0.38066, 0.47583, 0.2855)


def test_color_when_intersection_behind_ray():
    w = rt.World.default()
    outer = w.objects[0]
    outer.material.ambient = 1
    inner = w.objects[1]
    inner.material.ambient = 1
    r = rt.Ray(rt.Point(0, 0, 0.75), rt.Vector(0, 0, -1))
    c = w.color_at(r)
    assert c == inner.material.pattern.color


def test_no_shadow_when_point_and_light_not_collinear():
    w = rt.World.default()
    p = rt.Point(0, 10, 0)
    assert not w.is_shadowed(p)


def test_shadow_if_object_between_point_and_light():
    w = rt.World.default()
    p = rt.Point(10, -10, 10)
    assert w.is_shadowed(p)


def test_no_shadow_when_object_behind_the_light():
    w = rt.World.default()
    p = rt.Point(-20, 20, -20)
    assert not w.is_shadowed(p)


def test_no_shadow_when_object_behind_the_point():
    w = rt.World.default()
    p = rt.Point(-2, 2, -2)
    assert not w.is_shadowed(p)


def test_shade_hit_is_given_intersection_in_shadow():
    w = rt.World()
    w.lightSource = rt.PointLight(rt.Point(0, 0, -10), rt.Color(1, 1, 1))
    s1 = rt.Sphere()
    w.objects.append(s1)
    s2 = rt.Sphere()
    s2.set_transform(rt.translation(0, 0, 10))
    w.objects.append(s2)
    r = rt.Ray(rt.Point(0, 0, 5), rt.Vector(0, 0, 1))
    i = rt.Intersection(4, s2)
    comps = rt.prepare_computations(i, r)
    c = w.shade_hit(comps)
    assert c == rt.Color(0.1, 0.1, 0.1)
