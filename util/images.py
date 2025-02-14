
import io

import numpy as np
import pyray as rl
import requests
from PIL import Image
from cffi import FFI

from util.exceptions import ImgApiException

ffi = FFI()


def __is_valid_hexa_code(code: str) -> bool:
    """
    Checks if a code is a valid hexadecimal color.

    :param code:
    :return: True if the code is a valid hexadecimal color. False otherwise.
    """

    # obviously invalid case
    if len(code) != 8:
        return False

    # checks if each character is a valid base-16 digit
    # if the digit is valid, add True, else False
    # finally, checks if all the digits are valid.
    valid = all(
        (('0' <= c <= '9') or
         ('a' <= c <= 'f') or
         ('A' <= c <= 'F'))
        for c in code
    )

    # return the validity
    return valid


def __hex_to_rgba(code: str) -> tuple[int, ...]:
    """
    Converts a hexadecimal color code to an RGBA tuple.

    :param code:
    :return: The RGBA tuple.
    """

    # iterates through the hexadecimal code 2 characters at a time.
    # converts the string into an integer, interpreting it as a base-16 number.
    # add it to a tuple.
    # return the resulting color tuple.
    return tuple(int(code[i:i + 2], base=16) for i in (0, 2, 4, 6))


def parse_hex_color(color: str) -> rl.Color:
    """
    Converts a color string into a rl.Color object.

    :param color: Color string in r,g,b,a (NO SPACES)
    :return:
    """

    # invalid hexadecimal
    if not __is_valid_hexa_code(color):

        err_data = {"code": 400, "message": "Invalid color code"}

        raise ImgApiException("Hexadecimal parser error", err_data)

    # convert hexadecimal to rgba
    values = __hex_to_rgba(color)

    # generate raylib color
    return rl.Color(*values)


def get_image_bytes_as_png(image: rl.Image) -> bytes:
    """
    Returns the image bytes in PNG format.

    :param image: The image (rl.Image) to convert to PNG.
    :return: Image in PNG format.
    """

    # extract the raw image bytes. The default type is `void*`.
    # cast to `unsigned char*` so that the pixel data can be accessed.
    data = ffi.cast("unsigned char*", image.data)

    # converts the raw buffer to a 2D array of pixels.
    # `ffi.unpack` is used to extract the raw image data stored in 'data'.
    # 'uint8' is used as the byte values are known to be 8-bit unsigned integers.
    # the `.reshape()` is called as height, width, then 4, as numpy uses row-major matrices.
    # the 4 is due to the colors being RGBA values.
    pixels = (np.array(ffi.unpack(data, image.width * image.height * 4), dtype='uint8')
                .reshape(image.height, image.width, 4))

    # convert the raw image bytes to the PNG format.
    with io.BytesIO() as bytes_arr:
        # get the raw `bytes` array
        img: Image = Image.fromarray(pixels, "RGBA")
        img.save(bytes_arr, "png")
        png: bytes = bytes_arr.getvalue()

    # return the PNG data.
    return png


def get_image_bytes_as_png_rl(image: rl.Image) -> bytes:
    size = 0
    img_data = rl.export_image_to_memory(image, ".png", size)

    print(size)

    return bytes(ffi.unpack(img_data, image.width * image.height))


class ImageFormatMagicNumbers:
    """
    The image format prefix/magic numbers. Currently only supports PNG, JPG, and BMP. The format is checked through the
    image's file signature.
    """

    PNG = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
    JPG = bytes([0xFF, 0xD8, 0xFF])
    BMP = bytes([0x42, 0x4D])


def _get_image_format(dat: bytes) -> str:
    """
    Get the image format.

    :param dat: the image bytes.
    """

    if dat.startswith(ImageFormatMagicNumbers.PNG):
        return ".png"
    elif dat.startswith(ImageFormatMagicNumbers.JPG):
        return ".jpg"
    elif dat.startswith(ImageFormatMagicNumbers.BMP):
        return ".bmp"
    else:
        err_dat = {"code": 415, "message": "Unsupported image format."}
        raise ImgApiException("Unsupported image format.", err_dat)


def load_image_from_url(url: str) -> rl.Image:
    """
    Loads an image from an url. Url must be a direct link to the image.

    :param url: The url to load the image from. Must be a direct link to the image.
    :return: The loaded image.
    """

    response = requests.get(url)

    if response.status_code != 200:
        err_dat = {
            "code": 502,
            "message": f"Failed to fetch image, portal gave: {response.status_code}: {response.text}."
        }
        raise ImgApiException("Failed to fetch image.", err_dat)

    dat = response.content
    img_format = _get_image_format(dat)

    img = rl.load_image_from_memory(img_format, response.content, len(response.content))

    if img_format != ".png":
        # solution to non-png formats looking strange

        canvas = rl.gen_image_color(img.width, img.height, rl.WHITE)
        rect = rl.Rectangle(0, 0, img.width, img.height)
        rl.image_draw(canvas, img, rect, rect, rl.WHITE)

        return canvas

    return img
