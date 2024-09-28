from .tuples import Point, Vector, Color
from .canvas import Canvas
from .transformations import rotation_z, translation
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

def main():

    #canvas = draw_trajectory_of_projectile_chapter_two()
    canvas = draw_clock_chapter_four()

    ppm = canvas.convert_to_ppm()

    with open("output.ppm", "w") as text_file:
        text_file.write(ppm)


if __name__ == "__main__":
    main()
