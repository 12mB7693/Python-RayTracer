from .tuples import Point, Color
from .materials import Material

class PointLight:
    def __init__(self, position: Point, intensity: Color, material: Material = None) -> None:
        self.position = position
        self.intensity = intensity
        if material is None:
            self.material = Material()
        else:
            self.material = material
