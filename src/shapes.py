from .ray import Ray
from .tuples import Point, Vector
from .matrix import create_identity_matrix, Matrix
from .materials import Material
import math


class Shape:
    pass


class Intersection:
    def __init__(self, t, shape: Shape) -> None:
        self.t = t
        self.shape = shape

class IntersectionInfo(Intersection):
    def __init__(self, intersection: Intersection):
        super().__init__(intersection.t, intersection.shape)
        self.point = None
        self.eyev = None
        self.normalv = None
        self.inside = False

def prepare_computations(intersection: Intersection, ray: Ray) -> IntersectionInfo:
    comps = IntersectionInfo(intersection)
    comps.eyev = -ray.direction
    comps.point = ray.position(comps.t)
    comps.normalv = comps.shape.normal_at(comps.point)
    if comps.normalv.dot(comps.eyev) < 0:
        comps.inside = True
        comps.normalv = -comps.normalv
    return comps


def hit(intersections: list[Intersection]):
    pos_intersections = [i for i in intersections if i.t > 0]
    if len(pos_intersections) == 0:
        return None
    else:
        return min(pos_intersections, key=lambda intersection: intersection.t)
    # return min(intersections, key=lambda intersection : intersection.t)


class Sphere(Shape):
    def __init__(self):
        self.transform = create_identity_matrix()
        self.material = Material()

    def set_transform(self, transform: Matrix) -> None:
        self.transform = transform

    def normal_at(self, world_point: Point) -> Vector:
        object_point = self.transform.inverse().multiply(world_point)
        object_normal = object_point
        world_normal = self.transform.inverse().transpose().multiply(object_normal)
        world_normal.w = 0
        return world_normal.normalize()

    def intersect(self, ray: Ray) -> list[Intersection]:
        ray = self.transform.inverse().multiply(ray)
        sphere_to_ray = ray.origin - Point(0, 0, 0)
        a = ray.direction.dot(ray.direction)
        b = 2 * ray.direction.dot(sphere_to_ray)
        c = sphere_to_ray.dot(sphere_to_ray) - 1
        discriminant = b * b - 4 * a * c

        if discriminant < 0:
            return []

        t1 = (-b - math.sqrt(discriminant)) / (2 * a)
        t2 = (-b + math.sqrt(discriminant)) / (2 * a)
        return [Intersection(t1, self), Intersection(t2, self)]
