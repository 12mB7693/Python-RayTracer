from math import pi, sqrt

import raytracer as rt


def test_normal_at_x_axis():
    """
    Test the normal on a sphere at a point on the x axis
    """
    s = rt.Sphere()
    normal = s.normal_at(rt.Point(1, 0, 0))
    assert normal == rt.Vector(1, 0, 0)


def test_normal_at_y_axis():
    s = rt.Sphere()
    normal = s.normal_at(rt.Point(0, 1, 0))
    assert normal == rt.Vector(0, 1, 0)


def test_normal_at_z_axis():
    s = rt.Sphere()
    normal = s.normal_at(rt.Point(0, 0, 1))
    assert normal == rt.Vector(0, 0, 1)


def test_normal_at_nonaxial_point():
    s = rt.Sphere()
    normal = s.normal_at(rt.Point(1 / sqrt(3), 1 / sqrt(3), 1 / sqrt(3)))
    assert normal == rt.Vector(1 / sqrt(3), 1 / sqrt(3), 1 / sqrt(3))


def test_normal_is_normalized_vector():
    s = rt.Sphere()
    normal = s.normal_at(rt.Point(1 / sqrt(3), 1 / sqrt(3), 1 / sqrt(3)))
    assert normal == normal.normalize()


def test_normal_on_translated_sphere():
    s = rt.Sphere()
    s.set_transform(rt.translation(0, 1, 0))
    normal = s.normal_at(rt.Point(0, 1.70711, -0.70711))
    print(normal.z)
    assert normal == rt.Vector(0, 0.70711, -0.70711)


def test_normal_on_transformed_sphere():
    s = rt.Sphere()
    s.set_transform(rt.scaling(1, 0.5, 1).multiply(rt.rotation_z(pi / 5)))
    normal = s.normal_at(rt.Point(0, 1 / sqrt(2), -1 / sqrt(2)))
    assert normal == rt.Vector(0, 0.97014, -0.24254)


def test_default_material_of_sphere():
    s = rt.Sphere()
    m = rt.Material()
    assert m == s.material


def test_set_material_of_sphere():
    s = rt.Sphere()
    m = rt.Material()
    m.ambient = 1
    s.material = m
    assert s.material == m


def test_computation_preparation():
    r = rt.Ray(rt.Point(0, 0, -5), rt.Vector(0, 0, 1))
    shape = rt.Sphere()
    i = rt.Intersection(4, shape)
    info = rt.prepare_computations(i, r)
    assert info.intersection.t == i.t
    assert info.intersection.shape == i.shape
    assert info.point == rt.Point(0, 0, -1)
    assert info.eyev == rt.Vector(0, 0, -1)
    assert info.normalv == rt.Vector(0, 0, -1)


def test_intersection_occurs_on_the_outside():
    r = rt.Ray(rt.Point(0, 0, -5), rt.Vector(0, 0, 1))
    shape = rt.Sphere()
    i = rt.Intersection(4, shape)
    comps = rt.prepare_computations(i, r)
    assert not comps.inside


def test_intersection_occurs_on_the_inside():
    r = rt.Ray(rt.Point(0, 0, 0), rt.Vector(0, 0, 1))
    shape = rt.Sphere()
    i = rt.Intersection(1, shape)
    comps = rt.prepare_computations(i, r)
    assert comps.point == rt.Point(0, 0, 1)
    assert comps.eyev == rt.Vector(0, 0, -1)
    assert comps.inside
    assert comps.normalv == rt.Vector(0, 0, -1)


def test_hit_should_offset_the_point():
    r = rt.Ray(rt.Point(0, 0, -5), rt.Vector(0, 0, 1))
    s = rt.Sphere()
    s.set_transform(rt.translation(0, 0, 1))
    i = rt.Intersection(5, s)
    comps = rt.prepare_computations(i, r)
    assert comps.over_point.z < -rt.ABS_TOL / 2
    assert comps.point.z > comps.over_point.z


def test_plane_normal_at():
    p = rt.Plane()
    n1 = p.shape_specific_normal_at(rt.Point(0, 0, 0))
    n2 = p.shape_specific_normal_at(rt.Point(10, 0, -10))
    n3 = p.shape_specific_normal_at(rt.Point(-5, 0, 150))
    assert n1 == rt.Vector(0, 1, 0)
    assert n2 == rt.Vector(0, 1, 0)
    assert n3 == rt.Vector(0, 1, 0)


def test_intersect_ray_parallel_to_plane():
    p = rt.Plane()
    r = rt.Ray(rt.Point(0, 10, 0), rt.Vector(0, 0, 1))
    xs = p.shape_specific_intersect(r)
    assert xs == []


def test_intersect_ray_coplanar_to_plane():
    p = rt.Plane()
    r = rt.Ray(rt.Point(0, 0, 0), rt.Vector(0, 0, 1))
    xs = p.shape_specific_intersect(r)
    assert xs == []


def test_intersect_plane_from_above():
    p = rt.Plane()
    r = rt.Ray(rt.Point(0, 1, 0), rt.Vector(0, -1, 0))
    xs = p.shape_specific_intersect(r)
    assert len(xs) == 1
    assert xs[0].t == 1
    assert xs[0].shape == p


def test_intersect_plane_from_below():
    p = rt.Plane()
    r = rt.Ray(rt.Point(0, -1, 0), rt.Vector(0, 1, 0))
    xs = p.shape_specific_intersect(r)
    assert len(xs) == 1
    assert xs[0].t == 1
    assert xs[0].shape == p


def test_texture_transform():
    s = rt.Sphere()
    assert s.texture_transform(rt.Point(0, 0, 1)) == (0.75, 0.5)
    assert s.texture_transform(rt.Point(0, 0, -1)) == (0.25, 0.5)
