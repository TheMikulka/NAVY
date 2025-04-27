from PIL import Image
import colorsys
from FractalGenerator import FractalGenerator

class MandelbrotSet(FractalGenerator):
    def generate(self, x_min, x_max, y_min, y_max):
        image = Image.new("RGB", (self.width, self.height))
        pixels = image.load()

        for x in range(self.width):
            for y in range(self.height):
                zx = x * (x_max - x_min) / self.width + x_min
                zy = y * (y_max - y_min) / self.height + y_min
                c = complex(zx, zy)
                z = 0
                i = 0
                while abs(z) <= 2 and i < self.max_iter:
                    z = z * z + c
                    i += 1
                hue = int(255 * i / self.max_iter)
                color = tuple(int(c * 255) for c in colorsys.hsv_to_rgb(hue / 255.0, 1, i < self.max_iter))
                pixels[x, y] = color
        return image
