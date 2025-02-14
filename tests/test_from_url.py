import pyray as rl

from util import images


if __name__ == '__main__':
    rl.init_window(800, 600, "test window")

    img = images.load_image_from_url("https://i.imgur.com/ufXai2Z.png")
    tex = rl.load_texture_from_image(img)

    while not rl.window_should_close():
        rl.begin_drawing()

        rl.draw_texture(tex, 0, 0, rl.WHITE)

        rl.end_drawing()

    rl.close_window()
