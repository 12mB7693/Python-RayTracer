from src.raytracer import Canvas, Color


def test_canvas_dimensions():
    height = 20
    width = 10
    canvas = Canvas(width, height)
    assert canvas.width == width
    assert canvas.height == height
    assert len(canvas.pixels) == width * height


def test_canvas_pixel_at():
    height = 20
    width = 10
    canvas = Canvas(width, height)
    assert canvas.pixel_at(0, 0) == Color(0, 0, 0)
    assert canvas.pixel_at(width - 1, height - 1) == Color(0, 0, 0)


def test_canvas_initialization():
    height = 20
    width = 10
    canvas = Canvas(width, height)
    for y in range(height):
        for x in range(width):
            assert canvas.pixel_at(x, y) == Color(0, 0, 0)


def test_canvas_write_pixel():
    canvas = Canvas(width=10, height=20)
    color = Color(1, 0, 0)
    canvas.write_pixel(2, 3, color)
    assert canvas.pixel_at(2, 3) == color


def test_ppm_last_line_is_newline():
    canvas = Canvas(5, 3)
    ppm = canvas.convert_to_ppm()
    assert ppm.endswith("\n")


def test_break_long_lines_ppm():
    pass
    # canvas = Canvas(10, 2, Color(1, 0.8, 0.6))
    # ppm = canvas.convert_to_ppm()
    # for index, line in enumerate(ppm.splitlines()):
    #     if index == 3 or index == 5:
    #         assert line == "255 204 153 255 204 153 255 204 153 255 204 153 255 204 153 255 204 "
    #     if index == 4 or index == 6:
    #         assert line == "153 255 204 153 255 204 153 255 204 153 255 204 153 "


def test_ppm():
    canvas = Canvas(width=5, height=3)
    c1 = Color(1.5, 0, 0)
    c2 = Color(0, 0.5, 0)
    c3 = Color(-0.5, 0, 1)
    canvas.write_pixel(0, 0, c1)
    canvas.write_pixel(2, 1, c2)
    canvas.write_pixel(4, 2, c3)
    ppm = canvas.convert_to_ppm()

    for index, line in enumerate(ppm.splitlines()):
        if index == 0:
            assert line == "P3"
        elif index == 1:
            assert line == "5 3"
        elif index == 2:
            assert line == "255"
        elif index == 3:
            assert line == "255 0 0 0 0 0 0 0 0 0 0 0 0 0 0 "
        elif index == 4:
            assert line == "0 0 0 0 0 0 0 128 0 0 0 0 0 0 0 "
        elif index == 5:
            assert line == "0 0 0 0 0 0 0 0 0 0 0 0 0 0 255 "
