"""
This file contains basic rendering tasks for the server, to check if the server is up and running.

MIT License

Copyright (c) 2024 plurb

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from util import images

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from renderer import basic

router = APIRouter()


@router.get(
    "/square/{width}/{height}/{color}",
    responses={
        200: {
            "content": {"image/png": {}}
        },
        500: {
            "message": ""
        }
    },
    response_class=Response
)
async def square(width: int, height: int, color: str) -> Response:
    """
    Generates a 'square' image with the specified width and height and color.

    :param width: Width, integer.
    :param height: Height, integer.
    :param color: RGBA hexadecimal color.
    :return: Response containing the generated image.
    """

    # generate raylib color
    img = basic.square(width, height, color)

    return Response(content=img, media_type='image/png')


@router.get(
    path="/checkered/{width}/{height}/{checks_x}/{checks_y}/{col1}/{col2}",
    responses={
        200: {
            "content": {"image/png": {}}
        },
        500: {
            "message": ""
        }
    },
    response_class=Response
)
async def checkered(width: int, height: int, checks_x: int, checks_y: int, col1: str, col2: str) -> Response:
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

    img = basic.checkered(width, height, checks_x, checks_y, col1, col2)

    return Response(content=img, media_type='image/png')


@router.get(
    path="/perlin/{width}/{height}/{offset_x}/{offset_y}/{scale}",
    responses={
        200: {
            "content": {"image/png": {}}
        },
        500: {
            "message": ""
        }
    },
    response_class=Response
)
async def perlin(width: int, height: int, offset_x: int, offset_y: int, scale: float) -> Response:
    """
    Generates a perlin noise image.

    :param width: Width of the image.
    :param height: Height of the image.
    :param offset_x: Noise offset, x-axis.
    :param offset_y: Noise offset, y-axis.
    :param scale: Noise scale.
    :return: The image response.
    """

    # generate the image
    img = basic.perlin(width, height, offset_x, offset_y, scale)

    return Response(content=img, media_type='image/png')


@router.get(
    path="/circle/{width}/{height}/{position_x}/{position_y}/{radius}/{color}/{bg}",
    responses={
        200: {
            "content": {"image/png": {}}
        },
        500: {
            "message": ""
        }
    },
    response_class=Response
)
async def circle(width: int,
                 height: int,
                 position_x: int,
                 position_y: int,
                 radius: float,
                 color: str,
                 bg: str
                 ) -> Response:
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

    img = basic.circle(width, height, position_x, position_y, radius, color, bg)

    return Response(content=img, media_type='image/png')


@router.get(
    path="/from_url/",
    responses={
        200: {
            "content": {"image/png": {}}
        },
        500: {
            "message": ""
        }
    },
    response_class=Response
)
def from_url(url: str = "") -> Response:
    """
    Responds with the image.

    :param url: Link to the image. Must be a direct link. Supported formats: png, jpg, webp
    :return: The image response.
    """

    if not url:
        raise HTTPException(status_code=400, detail="Invalid URL")

    img = images.load_image_from_url(url)
    img_data = images.get_image_bytes_as_png(img)

    return Response(content=img_data, media_type='image/png')
