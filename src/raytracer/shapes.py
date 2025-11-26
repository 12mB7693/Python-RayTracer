from __future__ import annotations

import abc
import math
from dataclasses import dataclass

from .materials import Material
from .matrix import Matrix, create_identity_matrix
from .ray import Ray
from .tuples import ABS_TOL, Point, Vector


class Shape(metaclass=abc.ABCMeta):
    def __init__(self):
        self.transform = create_identity_matrix()
        self.material = Material()

    def set_transform(self, transform: Matrix) -> None:
        self.transform = transform

    def intersect(self, ray: Ray) -> list[Intersection]:
        """
        :param Ray ray: ray in world coordinates
        """
        # transform ray from world to object space
        ray = self.transform.inverse().multiply(ray)
        return self.shape_specific_intersect(ray)

    def normal_at(self, world_point: Point) -> Vector:
        object_point = self.transform.inverse().multiply(world_point)
        object_normal = self.shape_specific_normal_at(object_point)
        world_normal = self.transform.inverse().transpose().multiply(object_normal)
        return world_normal.normalize()

    @abc.abstractmethod
    def shape_specific_intersect(self, ray: Ray) -> list[Intersection]:
        pass

    @abc.abstractmethod
    def shape_specific_normal_at(self, object_point: Point) -> Vector:
        pass


@dataclass
class Intersection:
    t: float = 0.0
    shape: Shape = None


@dataclass
class IntersectionInfo:
    intersection: Intersection = None
    point: Point = None
    eyev: Vector = None
    normalv: Vector = None
    inside: bool = False
    over_point: Point = None


def prepare_computations(intersection: Intersection, ray: Ray) -> IntersectionInfo:
    eyev = -ray.direction
    point = ray.position(intersection.t)
    normalv = intersection.shape.normal_at(point)
    inside = False
    if normalv.dot(eyev) < 0:
        inside = True
        normalv = -normalv
    over_point = point + normalv * ABS_TOL
    info = IntersectionInfo(intersection, point, eyev, normalv, inside, over_point)
    return info


def hit(intersections: list[Intersection]):
    pos_intersections = [i for i in intersections if i.t > 0]
    if len(pos_intersections) == 0:
        return None
    else:
        return min(pos_intersections, key=lambda intersection: intersection.t)
    # return min(intersections, key=lambda intersection : intersection.t)


class Sphere(Shape):
    def __init__(self):
        super().__init__()

    def texture_transform(self, point: Point) -> tuple[float, float]:
        """

        point: on unit sphere

        """
        theta = math.acos(point.y)
        phi = math.atan2(point.z, point.x)
        u = (phi + math.pi) / (2 * math.pi)
        v = theta / math.pi
        return (u, v)

    def shape_specific_normal_at(self, object_point: Point) -> Vector:
        object_normal = Vector(object_point.x, object_point.y, object_point.z)
        return object_normal

    def shape_specific_intersect(self, ray: Ray) -> list[Intersection]:
        # ray = self.transform.inverse().multiply(ray) # transform ray to object space
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


class Plane(Shape):
    def shape_specific_normal_at(self, object_point: Point) -> Vector:
        return Vector(0, 1, 0)

    def shape_specific_intersect(self, ray: Ray) -> list[Intersection]:
        if abs(ray.direction.y) < ABS_TOL:
            return []

        t = -ray.origin.y / ray.direction.y
        return [Intersection(t, self)]
