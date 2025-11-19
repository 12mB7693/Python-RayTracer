from .shapes import Sphere, Intersection, IntersectionInfo, prepare_computations, hit
from .materials import Material, lighting
from .tuples import Color, Point
from .transformations import scaling
from .ray import Ray
from .lights import PointLight

class World:
    def __init__(self):
        self.objects = []
        self.lightSource = None

    @classmethod
    def default(cls):
        w = cls()
        s1 = Sphere()
        s1.material = Material(color=Color(0.8, 1, 0.6), diffuse=0.7, specular=0.2)
        w.objects.append(s1)
        s2 = Sphere()
        s2.set_transform(scaling(0.5, 0.5, 0.5))
        w.objects.append(s2)
        w.lightSource = PointLight(Point(-10, 10, -10), Color(1, 1, 1))
        return w

    def intersect(self, r: Ray) -> list[Intersection]:
        intersections = []
        for object in self.objects:
            intersections += object.intersect(r)
        intersections.sort(key=lambda intersection: intersection.t)
        return intersections

    def shade_hit(self, comps: IntersectionInfo) -> Color:
        return lighting(comps.shape.material, self.lightSource, comps.point, comps.eyev, comps.normalv)

    def color_at(self, r: Ray) -> Color:
        intersections = self.intersect(r)
        intersection = hit(intersections)
        if intersection is None:
            return Color(0, 0, 0)
        else:
            comps = prepare_computations(intersection, r)
            return self.shade_hit(comps)
