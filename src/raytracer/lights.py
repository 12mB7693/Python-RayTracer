from .tuples import Color, Point

# from .materials import Material


class PointLight:
    def __init__(
        self,
        position: Point,
        intensity: Color,  # , material: Material = None
    ) -> None:
        self.position = position
        self.intensity = intensity
        # if material is None:
        #    self.material = Material()
        # else:
        #    self.material = material

    def __eq__(self, value):
        if isinstance(value, PointLight):
            return (
                value.position == self.position and value.intensity == self.intensity
                # and value.material == self.material
            )
        else:
            return False
