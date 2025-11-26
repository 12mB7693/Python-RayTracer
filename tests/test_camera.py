import math

import raytracer as rt


def test_camera_constructor():
    hsize = 160
    vsize = 120
    fov = math.pi / 2
    c = rt.Camera(hsize, vsize, fov)
    assert c.hsize == 160
    assert c.vsize == 120
    assert c.fov == math.pi / 2
    assert c.transform == rt.create_identity_matrix()


def test_pixel_size_horizontal_canvas():
    c = rt.Camera(200, 125, math.pi / 2)
    assert math.isclose(c.pixel_size, 0.01, abs_tol=rt.ABS_TOL)


def test_pixel_size_vertical_canvas():
    c = rt.Camera(125, 200, math.pi / 2)
    print(c.pixel_size)
    assert math.isclose(c.pixel_size, 0.01, abs_tol=rt.ABS_TOL)


def test_ray_through_center_of_canvas():
    c = rt.Camera(201, 101, math.pi / 2)
    r = c.ray_for_pixel(100, 50)
    assert r.origin == rt.Point(0, 0, 0)
    assert r.direction == rt.Vector(0, 0, -1)


def test_ray_through_corner_of_canvas():
    c = rt.Camera(201, 101, math.pi / 2)
    r = c.ray_for_pixel(0, 0)
    assert r.origin == rt.Point(0, 0, 0)
    assert r.direction == rt.Vector(0.66519, 0.33259, -0.66851)


def test_ray_when_camera_transformed():
    c = rt.Camera(201, 101, math.pi / 2)
    c.transform = rt.rotation_y(math.pi / 4).multiply(rt.translation(0, -2, 5))
    r = c.ray_for_pixel(100, 50)
    assert r.origin == rt.Point(0, 2, -5)
    assert r.direction == rt.Vector(1 / math.sqrt(2), 0, -1 / math.sqrt(2))


def test_render_world():
    w = rt.World.default()
    c = rt.Camera(11, 11, math.pi / 2)
    c.transform = rt.view_transform(
        rt.Point(0, 0, -5), rt.Point(0, 0, 0), rt.Vector(0, 1, 0)
    )
    canvas = c.render(w)
    assert canvas.pixel_at(5, 5) == rt.Color(0.38066, 0.47583, 0.2855)
