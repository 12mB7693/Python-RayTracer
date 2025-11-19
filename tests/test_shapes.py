from src import *
from math import sqrt

def test_normal_at_x_axis():
    """
    Test the normal on a sphere at a point on the x axis
    """
    s = Sphere()
    normal = s.normal_at(Point(1, 0, 0))
    assert normal == Vector(1, 0 , 0)

def test_normal_at_y_axis():
    s = Sphere()
    normal = s.normal_at(Point(0, 1, 0))
    assert normal == Vector(0, 1 , 0)

def test_normal_at_z_axis():
    s = Sphere()
    normal = s.normal_at(Point(0, 0, 1))
    assert normal == Vector(0, 0 , 1)

def test_normal_at_nonaxial_point():
    s = Sphere()
    normal = s.normal_at(Point(1/sqrt(3), 1/sqrt(3), 1/sqrt(3)))
    assert normal == Vector(1/sqrt(3), 1/sqrt(3), 1/sqrt(3))

def test_normal_is_normalized_vector():
    s = Sphere()
    normal = s.normal_at(Point(1/sqrt(3), 1/sqrt(3), 1/sqrt(3)))
    assert normal == normal.normalize()

def test_normal_on_translated_sphere():
    s = Sphere()
    s.set_transform(translation(0, 1, 0))
    normal = s.normal_at(Point(0, 1.70711, -0.70711))
    print(normal.z)
    assert normal == Vector(0, 0.70711, -0.70711)

def test_normal_on_transformed_sphere():
    s = Sphere()
    s.set_transform(scaling(1, 0.5, 1).multiply(rotation_z(math.pi/5)))
    normal = s.normal_at(Point(0, 1/sqrt(2), - 1/sqrt(2)))
    assert normal == Vector(0, 0.97014, -0.24254)

def test_default_material_of_sphere():
    s = Sphere()
    m = Material()
    assert m == s.material

def test_set_material_of_sphere():
    s = Sphere()
    m = Material()
    m.ambient = 1
    s.material = m
    assert s.material == m

def test_computation_preparation():
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    shape = Sphere()
    i = Intersection(4, shape)
    comps = prepare_computations(i, r)
    assert comps.t == i.t
    assert comps.shape == i.shape
    assert comps.point == Point(0, 0, -1)
    assert comps.eyev == Vector(0, 0, -1)
    assert comps.normalv == Vector(0, 0, -1)

def test_intersection_occurs_on_the_outside():
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    shape = Sphere()
    i = Intersection(4, shape)
    comps = prepare_computations(i, r)
    assert comps.inside == False

def test_intersection_occurs_on_the_inside():
    r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
    shape = Sphere()
    i = Intersection(1, shape)
    comps = prepare_computations(i, r)
    assert comps.point == Point(0, 0, 1)
    assert comps.eyev == Vector(0, 0, -1)
    assert comps.inside == True
    assert comps.normalv == Vector(0, 0, -1)
