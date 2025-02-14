"""
Basic rendering tasks. Used to check if CLI and FastAPI server are operational.
"""

import pyray as rl

from util import images


def square(width: int, height: int, color: str) -> bytes:
    """
    Generates a 'square' image with the specified width and height and color.

    :param width: Width, integer.
    :param height: Height, integer.
    :param color: RGBA hexadecimal color.
    :return: Response containing the generated image.
    """

    # generate raylib color
    sq_color = images.parse_hex_color(color)

    # generate the image
    img = rl.gen_image_color(width, height, sq_color)

    # get the image bytes in png format
    img_data = images.get_image_bytes_as_png_rl(img)

    # clean up the image we don't need anymore
    rl.unload_image(img)

    return img_data


def checkered(width: int, height: int, checks_x: int, checks_y: int, col1: str, col2: str) -> bytes:
    """
    Generates a checkered image with the specified parameters.

    :param width: Width of the image.
    :param height: Height of the image.
    :param checks_x: Horizontal size of the squares.
    :param checks_y: Vertical size of the squares.
    :param col1: Color 1 of the squares, RGBA hexadecimal color.
    :param col2: Color 2 of the squares, RGBA hexadecimal color.
    :return: The image response.
    """

    # generate raylib colors
    color1 = images.parse_hex_color(col1)
    color2 = images.parse_hex_color(col2)

    # generate the image
    img = rl.gen_image_checked(width, height, checks_x, checks_y, color1, color2)

    # get the image bytes in png format
    img_data = images.get_image_bytes_as_png(img)

    # clean up the image we don't need anymore
    rl.unload_image(img)

    return img_data


def perlin(width: int, height: int, offset_x: int, offset_y: int, scale: float) -> bytes:
    """
    Generates a perlin noise image.

    :param width: Width of the image.
    :param height: Height of the image.
    :param offset_x: Noise offset, x-axis.
    :param offset_y: Noise offset, y-axis.
    :param scale: Noise scale.
    :return: The image response.
    """

    img = rl.gen_image_perlin_noise(width, height, offset_x, offset_y, scale)

    img_data = images.get_image_bytes_as_png(img)

    rl.unload_image(img)

    return img_data


async def circle(width: int,
                 height: int,
                 position_x: int,
                 position_y: int,
                 radius: float,
                 color: str,
                 bg: str
                 ) -> bytes:
    """
    Generates an image with a circle at position (x, y), with radius `radius` and color `color`.

    The background color is `bg`.

    :param width: Width of the image.
    :param height: Height of the image.
    :param position_x: Position of the circle, x-axis.
    :param position_y: Position of the circle, y-axis.
    :param radius: Radius of the circle.
    :param color: Color of the circle.
    :param bg: Background color.
    :return: The image response.
    """

    render_texture = rl.load_render_texture(width, height)
    bg_color = images.parse_hex_color(bg)
    circle_color = images.parse_hex_color(color)

    # drawing
    rl.begin_texture_mode(render_texture)

    rl.clear_background(bg_color)
    rl.draw_circle(position_x, position_y, radius, circle_color)

    rl.end_texture_mode()
    # end drawing

    # get the image
    img = rl.load_image_from_texture(render_texture.texture)

    # unload from VRAM
    rl.unload_render_texture(render_texture)

    # get the png data
    img_data = images.get_image_bytes_as_png(img)

    # unload the image
    rl.unload_image(img)

    return img_data
