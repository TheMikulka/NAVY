from PIL import Image
import colorsys
from FractalGenerator import FractalGenerator

class JuliaSet(FractalGenerator):
    def __init__(self, c=complex(-0.7, 0.27015), **kwargs):
        super().__init__(**kwargs)
        self.c = c

    def set_julia_constant(self, real, imag):
        self.c = complex(real, imag)

    def generate(self, x_min, x_max, y_min, y_max):
        image = Image.new("RGB", (self.width, self.height))
        pixels = image.load()

        for x in range(self.width):
            for y in range(self.height):
                zx = x * (x_max - x_min) / self.width + x_min
                zy = y * (y_max - y_min) / self.height + y_min
                z = complex(zx, zy)
                i = 0
                while abs(z) <= 2 and i < self.max_iter:
                    z = z * z + self.c
                    i += 1
                hue = int(255 * i / self.max_iter)
                color = tuple(int(c * 255) for c in colorsys.hsv_to_rgb(hue / 255.0, 1, i < self.max_iter))
                pixels[x, y] = color
        return image
