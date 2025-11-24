# RayTracer

![Python](https://img.shields.io/badge/python-3.12+-blue)
![uv](https://img.shields.io/badge/uv-package%20manager-brown)
![coverage](coverage.svg)


Install the Python package manager [uv](https://docs.astral.sh/uv/getting-started/installation/).

<!-- 

To install the requirements run the following command in the terminal 
```
uv pip install -r requirements.txt
# or
uv add --dev -r requirements-dev.txt
```

run uv sync regularly

-->

Run the raytracer: 

In the top folder run

```python
uv run python -m src.raytracer.main
```

## For developers

Run tests via
```
uv run python -m pytest
```

Check for errors and warnings via
```
uv run mypy -m src.raytracer.file_name
```

Compute Code Coverage locally
<!-- uv add --dev coverage-badge -->
```
uv run coverage-badge -o coverage.svg
```

## Credits / References

Buck, Jamis. "The ray tracer challenge: a test-driven guide to your first 3D renderer." (2019): 1-250.

Shirley, Peter, Michael Ashikhmin, and Steve Marschner. Fundamentals of computer graphics. AK Peters/CRC Press, 2009.

Earth Texture Image: “The Blue Marble: Land Surface, Ocean Color and Sea Ice,” NASA (MODIS / Terra satellite). Available at: https://visibleearth.nasa.gov/images/57730/the-blue-marble-land-surface-ocean-color-and-sea-ice
