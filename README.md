# RayTracer

![Python](https://img.shields.io/badge/python-3.12+-blue)
![uv](https://img.shields.io/badge/uv-brown)
[![Tests](https://github.com/12mB7693/Python-RayTracer/actions/workflows/tests.yml/badge.svg)](https://github.com/12mB7693/Python-RayTracer/actions/workflows/tests.yml)
[![code coverage](https://codecov.io/gh/12mB7693/Python-RayTracer/branch/main/graph/badge.svg)](https://codecov.io/gh/12mB7693/Python-RayTracer)


## Overview

This repository contains the implementation of a raytracer written in Python mainly based on the book _The ray tracer challenge: a test-driven guide to your first 3D renderer_ [^1].
So far, the implementation supports rendering spheres and planes with custom colors, patterns, and textures. The image below was rendered using a 2D projection of the earth [^2] as a texture.

![Rendering of the earth](imgs/earth_rendering.png)


<!--
## Implementation details
To improve performance, the custom matrix and vector arithmetic implementations have been replaced with NumPy’s built-in functions.
-->

## For developers

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



Run tests via
```
uv run python -m pytest
```

or run single tests with
```
uv run python -m pytest tests/test_module_name.py::test_name
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

[^1]: Buck, Jamis. "The ray tracer challenge: a test-driven guide to your first 3D renderer." (2019): 1-250.

<!-- Shirley, Peter, Michael Ashikhmin, and Steve Marschner. Fundamentals of computer graphics. AK Peters/CRC Press, 2009. -->

[^2]: Earth Texture Image: “The Blue Marble: Land Surface, Ocean Color and Sea Ice,” NASA (MODIS / Terra satellite). Available at: https://visibleearth.nasa.gov/images/57730/the-blue-marble-land-surface-ocean-color-and-sea-ice
