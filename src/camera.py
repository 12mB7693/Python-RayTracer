import math
from .matrix import create_identity_matrix
from .ray import Ray
from .tuples import Point
from .canvas import Canvas
from .world import World

class Camera:

    def __init__(self, hsize: int, vsize: int, fov: float):
        self.hsize = hsize
        self.vsize = vsize
        self.fov = fov
        self.transform = create_identity_matrix()
        self.compute_pixel_size()

    def compute_pixel_size(self) -> float:
        half_view = math.tan(self.fov/2)
        aspect = self.hsize / self.vsize

        if aspect >= 1:
            self.half_width = half_view
            self.half_height = half_view/aspect
        else:
            self.half_width = half_view*aspect
            self.half_height = half_view

        self.pixel_size = self.half_width * 2 / self.hsize

    def ray_for_pixel(self, px: int, py: int) -> Ray:
        xoffest = (px + 0.5) * self.pixel_size
        yoffset = (py + 0.5) * self.pixel_size

        world_x = self.half_width - xoffest
        world_y = self.half_height - yoffset

        pixel = self.transform.inverse().multiply(Point(world_x, world_y, -1))
        origin = self.transform.inverse().multiply(Point(0, 0, 0))
        direction = (pixel - origin).normalize()

        return Ray(origin, direction)

    def render(self, world: World) -> Canvas:
        canvas = Canvas(self.hsize, self.vsize)
        for y in range(self.vsize):
            for x in range(self.hsize):
                ray = self.ray_for_pixel(x, y)
                color = world.color_at(ray)
                canvas.write_pixel(x, y, color)

        return canvas
