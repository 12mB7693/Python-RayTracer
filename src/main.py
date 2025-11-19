from .tuples import Point, Vector, Color
from .canvas import Canvas
from .transformations import rotation_x, rotation_y, rotation_z, translation, shearing, scaling, view_transform
from .shapes import Sphere, hit
from .ray import Ray
from .lights import PointLight
from .materials import Material, lighting
from .world import World
from .camera import Camera
import math


class Projectile:
    def __init__(self, position: Point, veloctiy: Vector) -> None:
        self.position = position
        self.velocity = veloctiy


class Environment:
    def __init__(self, gravity: Vector, wind: Vector) -> None:
        self.gravity = gravity
        self.wind = wind


def tick(env, proj):
    proj.position = proj.position + proj.velocity
    proj.velocity = proj.velocity + env.gravity + env.wind

def draw_trajectory_of_projectile_chapter_two() -> Canvas:
    p = Projectile(Point(0, 1, 0), 11.25 * Vector(1, 1.8, 0).normalize())
    e = Environment(Vector(0, -0.1, 0), Vector(-0.01, 0, 0))
    canvas = Canvas(900, 550)

    tick_count = 0
    while p.position.y > 0:
        canvas.write_pixel(int(p.position.x), 550 - int(p.position.y), Color(1, 0, 0))
        tick(e, p)
        tick_count += 1
        print(f"Projectile position: ({p.position.x}, {p.position.y})")

    print(f"Tick count: {tick_count}")
    return canvas

def draw_clock_chapter_four():
    p = Point(80, 0, 0)
    canvas = Canvas(200, 200)
    points = []
    for i in range(12):
        points += [rotation_z(i * math.pi/6).multiply_tuple(p)]

    for p in points:
        p = translation(100, 100, 0).multiply_tuple(p)
        canvas.write_pixel(int(p.x), int(p.y), Color(1, 1, 1))

    return canvas

def simple_raytracer_chapter_five() -> Canvas:
    ray_origin = Point(0, 0, -5)
    wall_z = 10
    wall_size = 7.0
    canvas_pixels = 50
    pixel_size =  wall_size / canvas_pixels
    half = wall_size / 2

    canvas = Canvas(canvas_pixels, canvas_pixels)
    color = Color(1, 0, 0) # red
    shape = Sphere()
    transform = shearing(1, 0, 0, 0, 0, 0).multiply(scaling(0.5, 1, 1))
    shape.set_transform(transform)

    for y  in range(canvas_pixels - 1):
        world_y = half - pixel_size * y
        for x in range(canvas_pixels - 1):
            world_x = -half + pixel_size * x
            position = Point(world_x, world_y, wall_z)
            r = Ray(ray_origin, (position - ray_origin).normalize())
            xs = shape.intersect(r)
            if hit(xs) is not None:
                canvas.write_pixel(x, y, color)

    return canvas

def simple_raytracer_chapter_six() -> Canvas:
    ray_origin = Point(0, 0, -5)
    wall_z = 10
    wall_size = 7.0
    canvas_pixels = 100
    pixel_size =  wall_size / canvas_pixels
    half = wall_size / 2

    canvas = Canvas(canvas_pixels, canvas_pixels)
    color = Color(1, 0, 0) # red
    shape = Sphere()
    shape.material.color = Color(1, 0.2, 1)
    light = PointLight(Point(-10, 10, -10), Color(1, 1, 1))
    #transform = shearing(1, 0, 0, 0, 0, 0).multiply(scaling(0.5, 1, 1))
    #shape.set_transform(transform)

    for y  in range(canvas_pixels - 1):
        world_y = half - pixel_size * y
        for x in range(canvas_pixels - 1):
            world_x = -half + pixel_size * x
            position = Point(world_x, world_y, wall_z)
            r = Ray(ray_origin, (position - ray_origin).normalize())
            xs = shape.intersect(r)
            hit_result = hit(xs)
            if hit_result is not None:
                point = r.position(hit_result.t)
                normal = hit_result.shape.normal_at(point)
                eye = -r.direction
                color = lighting(hit_result.shape.material, light, point, eye, normal)
                canvas.write_pixel(x, y, color)

    return canvas

def simple_scene_chapter_seven():
    #ray_origin = Point(0, 0, -5)
    #wall_z = 10
    #wall_size = 7.0
    #canvas_pixels = 30
    #pixel_size =  wall_size / canvas_pixels
    #half = wall_size / 2

    #canvas = Canvas(canvas_pixels, canvas_pixels)

    floor = Sphere()
    floor.transform = scaling(10, 0.01, 10)
    floor.material = Material(color = Color(1, 0.9, 0.9), specular=0)

    left_wall = Sphere()
    left_wall.set_transform(translation(0, 0, 5).multiply(rotation_y(-math.pi/4))
                                                  .multiply(rotation_x(math.pi/2))
                                                  .multiply(scaling(10, 0.01, 10)))
    left_wall.material = floor.material

    right_wall = Sphere()
    right_wall.set_transform(translation(0, 0, 5).multiply(rotation_y(math.pi/4))
                                                 .multiply(rotation_x(math.pi/2))
                                                 .multiply(scaling(10, 0.01, 10)))
    right_wall.material = floor.material

    middle = Sphere()
    middle.set_transform(translation(-0.5, 1, 0.5))
    middle.material = Material(color=Color(0.1, 1, 0.5), diffuse=0.7, specular=0.3)

    right = Sphere()
    right.set_transform(translation(1.5, 0.5, -0.5).multiply(scaling(0.5, 0.5, 0.5)))
    right.material = Material(color=Color(0.5, 1, 0.1), diffuse=0.7, specular=0.3)

    left = Sphere()
    left.set_transform(translation(-1.5, 0.33, -0.75).multiply(scaling(0.33, 0.33, 0.33)))
    left.material = Material(color=Color(1, 0.8, 0.1), diffuse=0.7, specular=0.3)


    world = World()
    world.objects = [floor, left_wall, right_wall, right, middle, left]
    world.lightSource = PointLight(Point(-10, 10, -10), Color(1, 1, 1))

    camera = Camera(100, 50, math.pi/3)
    camera.transform = view_transform(Point(0, 1.5, -5), Point(0, 1, 0), Vector(0, 1, 0))
    canvas = camera.render(world)
    return canvas


def main():

    #canvas = draw_trajectory_of_projectile_chapter_two()
    #canvas = draw_clock_chapter_four()
    #canvas  = simple_raytracer_chapter_five()
    #canvas = simple_raytracer_chapter_six()
    canvas = simple_scene_chapter_seven()

    ppm = canvas.convert_to_ppm()

    with open("output.ppm", "w") as text_file:
        text_file.write(ppm)


if __name__ == "__main__":
    main()
